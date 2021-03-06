library(scales)


plotByYear<-function(){

	byear=data.frame()
	for(y in 2011:2016){
		tstep=0
		ipath=paste("projects/",y,sep="")
		ids=read.csv(paste(ipath,"/id.csv",sep=""))
		byear=rbind(byear,c(y,nrow(ids)))
	}
	colnames(byear)=c("year","modifications")
	png("year.png")
	plot(byear$modifications ~ byear$year,ylab="Nb of modifications",xlab="years",main="Modifications on page Project")
	dev.off()
}

plotNetwork<-function(mat,id="",...){
	#inp=colnames(mat)
	#out=rownames(mat)
	colnames(mat)=NA
	outWeigth = 1+apply(mat,1,sum)
	inWeigth = 1+apply(mat,2,sum)
	inPoints=1:length(inWeigth)
	outPoints=1:length(outWeigth)
	input=inPoints*4 #cbind(inPoints,names(inWeigth))
	output=outPoints*4+length(input) #cbind(outPoints,names(outWeigth))


	ptsize=4
	plot(input,rep(-1,length(inPoints)),cex=inWeigth,bty="n",ylim=c(-1.5,1.5),xlim=c(-10,max(input)+5),col=alpha("green",0.5),pch=20,xaxt="n",xlab="",yaxt="n", ylab="")
	text(input,rep(-1.03,length(inPoints))-.5,label=names(inWeigth),cex=.4,srt=60,c(1,1))
	points(output,rep(1,length(outPoints)),cex=outWeigth,col=alpha("dark blue",0.5),pch=20)
	text(output,rep(1.01,length(outPoints))+.5,label=names(outWeigth),cex=.4,srt=300,adj=c(1,1))
	text(-5,-1,"people")
	text(-5+length(input),1,"projects")
	text(0,0,id,cex=2)

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



#A function to print the graph of a given year 
printAllGraph<-function(year,mod){
	tstep=0
	ipath=paste("projects/",year,"/",sep="")
	opath=paste("bipartite/",year,"/",sep="")

	ids=read.csv(paste(ipath,"id.csv",sep=""))

	for( e in seq(1,nrow(ids),mod)){
		i=ids$id[e]
		ti=ids$time[e]
		filename=paste(ipath,i,"participation_matrix-filled.csv",sep="")
		print(filename)
		mat=read.csv(filename)#paste(ipath,ifile,sep=""))
		#rownames(mat)=mat[,1] anonymous
		#rownames(mat)=1:(nrow(mat)-1)
		mat=mat[,2:ncol(mat)]

		png(paste(opath,"bipartite-",i,".png",sep=""),width=2400,height=600,pointsize=17)
		par(mar=c(0,0,0,0))
		plotNetwork(mat,id=ti)
		dev.off()

	}
}

year=2016
mod=1

for( year in 2011:2016){
	printAllGraph(year,mod)
}
#the command to make the gif with all pictures:$ convert -dely 1 -loop 0 bipartite/*.png animation.gif
