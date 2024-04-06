# Set terminal to an appropriate one (e.g., 'png', 'svg', 'pdf', ...)
set terminal png size 800,600
set output 'plot_obj_time.png'

# Set labels for axes
set xlabel "# container objs"
set ylabel "blocking time (s)"
set y2label "# all live objs"

# Enable the right-hand side Y axis
set y2tics
set autoscale y2

# Tell Gnuplot which columns to use for which axes
set style data lines

# Plot the first line using the 1st and 2nd columns
plot 'data.txt' using 1:2 title '# all live objs' with lines, \
     '' using 1:3 title 'blocking time (s)' with lines axes x1y2
