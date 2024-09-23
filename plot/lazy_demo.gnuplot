set terminal pngcairo size 1200,500 enhanced font 'Verdana,10'
# enhanced font 'Verdana,10' size 12cm,8cm
# size 1200,500 enhanced font 'Verdana,10'
set output 'lazy_demo.png'
# font settings
# set title "Comparison of Graph500 and PageRank" font ',14'  # Increase title font size
set xlabel font ',14'  # Increase x-axis labels font size
set ylabel font ',14'  # Increase y-axis labels font size
set xtics font ',14'   # Increase x-axis tic numbers font size
set ytics font ',14'   # Increase y-axis tic numbers font size
set key font ',14'     # Increase legend font size

# set lmargin 5    # Left margin
# set rmargin 5    # Right margin
set tmargin 2    # Top margin
set bmargin 4    # Bottom margin

set multiplot layout 1,5

set yrange [1:1.23]
set xtics nomirror rotate by 45
set xtics offset -1.5, -2
set style data histogram
set style histogram cluster gap 1
set style fill pattern border -1
set grid ytics
set border 3
set boxwidth 0.8
set ylabel "Normalized Slowdown"
set ytics nomirror

# set lmargin 5
set rmargin 0
set label 1 "networkx\\_astar" at graph 0.65, graph 0.8 center font ',14'

set key inside top right

plot 'networkx_astar_lazy.dat' using 2:xtic(1) title 'eager', \
     '' using 3 title 'lazy'

unset label
unset ylabel
set ytics nomirror
set ytics format ""
set key inside top right

set label 2 "networkx\\_bellman" at graph 0.6, graph 0.8 center font ',14'

plot 'networkx_bellman_lazy.dat' using 2:xtic(1) title 'eager', \
     '' using 3 title 'lazy'

unset label
unset ylabel
set ytics nomirror
set ytics format ""
set key inside top right
set lmargin 1

set label 3 "networkx\\_bidirectional" at graph 0.55, graph 0.8 center font ',14'

plot 'networkx_bd_lazy.dat' using 2:xtic(1) title 'eager', \
     '' using 3 title 'lazy'

unset label
unset ylabel
set ytics nomirror
set ytics format ""
set key inside top right
set rmargin 0

set label 3 "networkx\\_kc" at graph 0.55, graph 0.8 center font ',14'

plot 'networkx_kc_lazy.dat' using 2:xtic(1) title 'eager', \
     '' using 3 title 'lazy'

unset label
unset ylabel
set ytics nomirror
set ytics format ""
set key inside top right
set lmargin 1
set rmargin 1

set label 3 "networkx\\_sp" at graph 0.55, graph 0.8 center font ',14'

plot 'networkx_sp_lazy.dat' using 2:xtic(1) title 'eager', \
     '' using 3 title 'lazy'

unset label
unset multiplot