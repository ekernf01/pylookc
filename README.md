## Leave-one-out knockoffs for efficient structure learning in Python

The framework of *Model-X knockoffs* and the corresponding R package `knockoff` together provide FDR control for subset selection in sparse regression models with multivariate Gaussian covariates (1). Model-X knockoffs have also been applied for structure learning (2) by leaving out each variable in turn. Previously, this required re-building knockoffs for each held-out variable, incurring a total cost scaling with the dimension to the fourth power. To facilitate progress in applications, especially in causal modeling of transcription, this package provides efficient free software for leave-one-out knockoff generation. 

Since knockoffs can be paired with arbitrary variable importance measures, the intended use case here is for when code to compute your variable importance measure of choice is more mature Python rather than R, as might be the case for many neural networks. HOWEVER, the main code-base for this project is in R -- please see the [`rlookc` package](https://github.com/ekernf01/rlookc) for proper detail -- and the Python version only takes care of the nastiest technical bottleneck relating to our specific work. You will have to do a lot of the work either using our code in R, or do it yourself in Python. 

The intended workflow is: 

- Efficiently generate the LOOKs in R and save them to disk
- Read them into python and compute variable importances in Python
- Control FDR by reading the result back into R, or by implementing the rest of the knockoff filter yourself in Python

The main advantage of this workflow: for very high-dimensional applications, this specific storage format is much more efficient than a naive approach. LOOKs can be algebraically decomposed and saved in O(ND) space, rather O(ND^2), where D is the data dimension and N is the number of observations. Re-assembling them is complicated and highly specific to our approach, so reassembly is implemented here. The remaining downstream steps of the knockoff filter are not as complicated and not as specific to our work, so with apologies they are not implemented here.

#### References

1. Candes, E., Fan, Y., Janson, L., & Lv, J. (2016). Panning for gold: Model-X knockoffs for high-dimensional controlled variable selection. arXiv preprint arXiv:1610.02351.
2. Zheng, Z., Zhou, J., Guo, X., & Li, D. (2018). Recovering the graphical structures via knockoffs. Procedia Computer Science, 129, 201-207.
