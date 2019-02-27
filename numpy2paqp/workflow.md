```java
run("Format converter", "opts={status:[],areMultipleFiles:true,paramFile:(C:\\Users\\baniu\\Documents\\Repos\\moving_shapes\\numpy2paqp\\test_data\\output_0.paQP)}");

run("Generate mask", "opts={binary:true,paramFile:(C:\\Users\\baniu\\Documents\\Repos\\moving_shapes\\numpy2paqp\\test_data\\output.QCONF)}");

run("ECMM Mapping", "opts={paramFile:(C:\\Users\\baniu\\Documents\\Repos\\moving_shapes\\numpy2paqp\\test_data\\output.QCONF)}");

selectWindow("output_snakemask.tif");


run("QuimP Analysis", "opts={trackColor:Summer,outlinePlot:Speed,sumCov:1.0,avgCov:0.0,mapRes:400,paramFile:(C:\\Users\\baniu\\Documents\\Repos\\moving_shapes\\numpy2paqp\\test_data\\output.QCONF)}");

run("Format converter", "opts={status:[map:coord,map:origin,map:ycoords,map:xcoords,map:motility,map:convexity,map:fluores],areMultipleFiles:true,paramFile:(C:\\Users\\baniu\\Documents\\Repos\\moving_shapes\\numpy2paqp\\test_data\\output.QCONF)}");
```
