Discretized Time Popularity to build a Time Popularity heatmap in Tableau

Created Time Column 10:00-22:00

Created Weekday Column 1-7 repeated as rows for each time column row

Created Total_RSVPs column
by summing RSVPs during time and weekday block over the year
=SUMIFS($C$2:$C$13861,$Q$2:$Q$13861,"<="&$W1,$R$2:$R$13861,">"&$W1,$O$2:$O$13861,$V1)

Created Percent_RSVPs column
by dividing Total_RSVPs by sum(Total_RSVPs)
=X1/SUM($C$2:$C$13861)

Created Percent_of_Max_RSVPs column
by dividing Percent_RSVPs by max(Percent_RSVPs)
=Y1/MAX(Y:Y)
