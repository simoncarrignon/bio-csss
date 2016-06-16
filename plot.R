
res=read.csv("people.txt",sep="\t")
mat=res[,3:7]
rownames(mat)=sapply(strsplit(as.character(res[,2]),"/"),function(x) return( x[length(x)])) #only two clean the name given by mallet
png("tree.png",1200,400)
par(mar=c(10,0,0,0))
plot(as.dendrogram(hclust(dist(mat)))) #plot of a clustering based on the distance calculated using the value for each topic
dev.off()
