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
    
