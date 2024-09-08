set datafile separator ','
set terminal png
set output output_file
set title wl_title
set xlabel "Time (s)"
set ylabel "Bandwidth (MB/s)"
plot input_file \
    using 1:2 title 'Bandwidth' with lines ls 1
    # '' using 1:3 title 'CXL' with lines ls 2
    # '' using 1:4 title 'sock0\_read' with lines ls 3, \
    # '' using 1:5 title 'sock0\_write' with lines ls 4, \