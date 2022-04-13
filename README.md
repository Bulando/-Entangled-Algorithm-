# EntangledAlgorithm

针对传统聚类算法在海关数据集上类簇大小取决于阈值设定、类簇无法准确划分的问题，本文在设定的阈值生成高密度类簇的前提下，将短文本聚类结果作为类簇文档进行聚合。由于深度学习神经网络对文档聚类的效果提升并不明显，因此本文回到类簇原始本有的关键词特征上提出了一种新的类簇聚合算法。相织算法通过遍历关键词和类簇之间的词频权值映射，以词频最大为主要原则，对映射之间的相容和不完全相容关系进行消解，形成了关键词与类簇完全解耦的一对多映射关系。相织算法基于类簇文档间最大关键词特征聚合形成新的类簇，提升了传统聚类算法在同义词聚合上表现。

Aiming at the problem that the traditional clustering algorithm could not accurately divide clusters on the customs data set, which depends on the threshold setting. In this thesis, short text clustering results are used as cluster documents for clustering under the premise of generating high-density clusters on the setting threshold. Since the deep learning neural network does not significantly improve the clustering effect of documents, this thesis proposes a new clusters mergings algorithm called EA(Entangled Algorithm) based on the original keyword frequency features of document clusters. By traversing the word frequency weight mapping between keywords and clusters. Under the principle of maximum word frequency, the compatible and not fully compatible relationships between mappings are eliminated, and the one-to-many mapping relationship of keywords and clusters is completely decoupled. Entagled Algorithm forms a new cluster based on the maximum keyword characteristics, which improves the performance of traditional clustering algorithm in synonym merging.

![image](https://user-images.githubusercontent.com/15541630/163118613-45ff6c63-7efe-4b53-be3a-1e170c19e2cd.png)

![image](https://user-images.githubusercontent.com/15541630/163118655-1186e14f-4d7e-4ccd-beec-aba016182560.png)
