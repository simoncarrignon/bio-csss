library(scales)
plotNetwork<-function(mat,city=""){
	inp=colnames(mat)
	out=rownames(mat)
	outWeigth = 1+apply(mat,1,sum)
	inWeigth = 1+apply(mat,2,sum)
	inPoints=1:length(inWeigth)
	outPoints=1:length(outWeigth)
	input=inPoints*4 #cbind(inPoints,names(inWeigth))
	output=outPoints*4+length(input) #cbind(outPoints,names(outWeigth))


	#plot(input[,1],rep(1,length(inPoints)),cex= sort(inWeigth)/max(inWeigth)*40,bty="n",ylim=c(-2.2,2),xlim=c(-10,215),col=alpha("dark green",0.5),pch=20,xaxt="n",xlab="",yaxt="n", ylab="")
	ptsize=4
	plot(input,rep(-1,length(inPoints)),cex=inWeigth,bty="n",ylim=c(-3.5,6.5),xlim=c(-10,max(input)+5),col=alpha("green",0.5),pch=20,xaxt="n",xlab="",yaxt="n", ylab="")
	text(input,rep(-1.03,length(inPoints))-.5,label=names(inWeigth),cex=.4,srt=60,c(1,1))
	points(output,rep(1,length(outPoints)),cex=outWeigth,col=alpha("dark blue",0.5),pch=20)
	text(output,rep(1.01,length(outPoints))+.5,label=names(outWeigth),cex=.4,srt=300,adj=c(1,1))
	text(-5,-1,"people")
	text(-5+length(input),1,"projects")

	cx0=c()
	cy0=c()
	cx1=c()
	cy1=c()

	if(nrow(mat)>0){
	for( i in 1:ncol(mat)){
		for(j in 1:(nrow(mat))){
			xp=output[j]
			yp=1
			xf=input[i]
			yf=-1
			#print(paste("i",i))
			#print(paste("j",j))
			if(mat[j,i]==1){
				segments(x0=xf,y0=yf,x1=xp,y1=yp,col=alpha("black",.3))
			}
		}
	}
	}
}


tstep=0
ipath="projects/2016/"
opath="bipartite/"
for( ifile in list.files(path=ipath,pattern=".+participation_matrix-filled.csv")){
	tstep=tstep+1
	if(tstep %% 10 == 0){
		mat=read.csv(paste(ipath,ifile,sep=""))
		print(ifile)
		rownames(mat)=mat[,1]
		mat=mat[,2:ncol(mat)]

		png(paste(opath,"bipartite-",tstep,".png",sep=""),width=2400,height=600,pointsize=17)
		par(mar=c(0,0,0,0))
		plotNetwork(mat)
		dev.off()
	mat=read.csv("projects/2016/61615participation_matrix-filled.csv")
	rownames(mat)=mat[,1]
	mat=mat[,2:ncol(mat)]
	png("tesst.png",width=2400,height=600,pointsize=17)
	par(mar=c(0,0,0,0))
	plotNetwork(mat)
	dev.off()
	}
}
#the command to make the gif with all pictures:$ convert -dely 1 -loop 0 bipartite/*.png animation.gif
