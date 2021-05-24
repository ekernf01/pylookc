import numpy as np
import os

#' Load result of saveCompactLooks
#'
def loadCompactLooks(savepath, filetype = "csv"):
  looks = {
    "knockoffs" : None,
    "groups" : None,
    "vars_to_omit" : [],
    "updates": []
  }
  if filetype == "csv":
    def do_load( thing ):
      my_file = os.path.join( savepath, thing + "." + filetype )
      return np.genfromtxt(my_file, delimiter=',', skip_header = 1, dtype = None, encoding = "UTF8")
      
  elif filetype == "h5":
    raise ValueError("Reading hdf5 is not implemented yet.\n")
  else:
    raise ValueError("Filetype must be 'csv' or 'h5'.\n")
  
  # Get stuff
  looks["vars_to_omit"] = do_load( "vars_to_omit") #This is from R, so it's 1-based!
  looks['knockoffs'] = do_load( "knockoffs" )
  # Handle irregular shape of groups and possible NULL specification of groups
  looks['groups'] = [[int(i) for i in s.split(" ")] for s in do_load( "groups") ]
  if len(looks['groups'])==0:
    looks['groups'] = None
  
  # Get updates as matrices
  temp = {}
  for field in [
    "mean_update1_left",
    "mean_update1_right",
    "mean_update2_left",
    "mean_update2_right",
    "sqrt_cov_update",
    "random"
  ]:
    temp[field] = do_load( field )
  
  # Reshape updates into the admittedly eccentric original format
  def fix_transpose(named_updates):
    for n in named_updates.keys():
      if "right" in n or "cov" in n:
        pass
      else:
        named_updates[n] = named_updates[n].T
    return named_updates
  
  looks["updates"] = [{} for k in looks['vars_to_omit']]
  for k in range(len(looks['vars_to_omit'])):
    looks['updates'][k] = fix_transpose({n:np.atleast_2d(temp[n][:,k]) for n in temp.keys()}) #take row or col??
  return looks


#' Alias for loadCompactLooks
#'
readCompactLooks = loadCompactLooks


#' Extract one update from the low-rank representation, while handling a tricky case properly.
#'
def getUpdateK(k, vars_to_omit, updates):
  correct_index = [i for i in range(len(vars_to_omit)) if vars_to_omit[i]==k][0] # Handle case when vars_to_omit is not 0, 1, 2, ... P-1
  return updates[correct_index]


#' Given the low-rank representations, update knockoffs to omit each variable.
#'
#' @param k variable to omit.
#' @param updates @param knockoffs @param vars_to_omit
#' Inputs should be from \code{loadCompactLooks} or from \code{generateLooks(..., output_type = 'knockoffs_compact'}.)
#' Those functions return a list with the same names as the necessary args.
#' @export
#'
def formAllLooks(knockoffs, vars_to_omit, updates):
    return [ formOneLook(knockoffs, vars_to_omit, updates, k) for k in vars_to_omit ] 
  


#' Given the low-rank representations, update knockoffs to omit one variable.
#'
#' @param k variable to omit.
#' @param updates @param knockoffs @param vars_to_omit
#' Inputs should be from \code{loadCompactLooks} or from \code{generateLooks(..., output_type = 'knockoffs_compact'}.)
#' Those functions return a list with the same names as the necessary args.
#' @export
#'
def formOneLook(knockoffs, vars_to_omit, updates, k):
  one_update = getUpdateK(k, vars_to_omit, updates)
  mask = [True for i in range(knockoffs.shape[1])]
  mask[k-1] = False # vars_to_omit is 1-indexed.
  return knockoffs[:,mask] + \
           getMeanUpdate(one_update) + \
           getRandomUpdate(one_update)
  

#' Output can be added to knockoffs to correct for removal of a variable.
#'
def getMeanUpdate(updates):
  return updates['mean_update1_left'] @ updates['mean_update1_right'] + \
         updates['mean_update2_left'] @ updates['mean_update2_right']
  

def getRandomUpdate(updates):
  return updates['random'] @ updates['sqrt_cov_update']

