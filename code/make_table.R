x <- read.csv("~/Downloads/Probgen abstract scoring - Session list.csv", header = FALSE)

## can't obviously use normal colour blind palette hexes
## but quick google "html colour picker"
## gives a good widget
## W+P, coffee, talks
## light purple, light orange, light green
cols <- c("#f1dcfa", "#faefdc", "#dcfae5")

## want e.g. this
## <tr bgcolor = "green">
##     <td>Welcome</td>
##     <td>Welcome</td>
##     <td>Welcome</td>
## <tr>

f <- function(xL, cols) {
    to_out <- NULL
    i <- 1
    for(i in 1:nrow(xL)) {
        to_out <- paste0(
            to_out,
            paste0('<tr bgcolor = "', cols[i], '">\n'),
            paste0("\t<td>", xL[i, 1], "</td>\n"),
            paste0("\t<td>", xL[i, 2], "</td>\n"),
            paste0("\t<td>", xL[i, 3], "</td>\n"),
            paste0('</tr>\n\n')
        )
    }
    cat(to_out)
}

f(
    xL = x[2:8, ],
    cols = cols[c(1, 2, 3, 2, 3, 2, 3)]
)
    
f(
    xL = x[11:17, ],
    cols = cols[c(1, 2, 3, 2, 3, 2, 3)]
)
    

f(
    xL = x[20:27, ],
    cols = cols[c(1, 3, 2, 3, 2, 3, 2, 1)]
)
    





##
## this bottom part is to add the talks
##
x2 <- read.csv("~/Downloads/Probgen abstract scoring - Talk list.csv", header = FALSE)

## <tr>
##       <td><i>  Talk 1</i></td>
##       <td><i>  Some person</i></td>
##       <td><i>  Some person's talk title</i></td>	
## </tr>

f <- function(xL, i) {
    to_out <- NULL
    for(j in 1:nrow(xL)) {
        to_out <- paste0(
            to_out,
            paste0("<tr>\n"),
            paste0('\t<td><i>Talk ', i[j], '</i></td>\n'),
            paste0("\t<td><i>", xL[j, "V6"], "</i></td>\n"),
            paste0("\t<td><i>", xL[j, "V11"], "</i></td>\n"),            
            paste0('</tr>\n\n')
        )
    }
    cat(to_out)
}


f(x2[4:6, ], 1:3)
f(x2[8:10, ], 4:6)
f(x2[12:14, ], 7:9)
f(x2[17:19, ], 10:12)
f(x2[21:23, ], 13:15)
f(x2[25:27, ], 16:18)
f(x2[29:30, ], 19:20)
f(x2[32:34, ], 21:23)
f(x2[36:38, ], 24:26)

