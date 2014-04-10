library(ggplot2)
files <- list.files(pattern=".csv$")
g <- 0
for(f in files)
{
    infile <- read.csv(paste(f),header=TRUE,sep=",")
    out <- ggplot(data=infile, aes(x=mem, y=core, fill=mhs)) + geom_tile() + scale_fill_gradientn(colours = rainbow(7))
    ggsave(out,filename=paste("clocks-", g, ".png", sep = ""))
    g <- g + 1
}
