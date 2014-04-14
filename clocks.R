library(ggplot2)
files <- list.files(pattern=".csv$")
for(f in files)
{
    gpu <- gsub(".*-(.*)\\..*", "\\1", c(f))
    infile <- read.csv(f, header=TRUE, sep=",")
    out <- ggplot(data=infile, aes(x=mem, y=core, fill=mhs)) + geom_tile() + scale_fill_gradientn(colours = rainbow(7))
    ggsave(out,filename=paste("clocks-", gpu, ".png", sep = ""))
}
