library(tidyverse)

shot_data <- read_csv("C:\\VS_Code\\NBA-Project\\shot_data.csv")

# Function to add team short to each shot instance
get_team_codes <- function(input_data) {
  output_data <- input_data %>%
    mutate(team_short = if_else(nchar(MATCHUP)==24, 
                          if_else(LOCATION=="H", 
                                  substr(MATCHUP,22,24), 
                                  substr(MATCHUP,16,18)), 
                          if_else(LOCATION=="H", 
                                  substr(MATCHUP,16,18), 
                                  substr(MATCHUP,24,26))))
  return(output_data)
}

# Split data on closest defender dist
get_split_dist_data <- function(input, dist) {
  smaller_data <- input %>%
    filter(CLOSE_DEF_DIST <= dist)
  larger_data <- input %>%
    filter(CLOSE_DEF_DIST > dist)
  
  return (list(smaller_data, larger_data))
}

# Get FG% for shots
get_split_fg <- function(input_data, dist_val) {
  split_data <- get_split_dist_data(input_data, dist_val)
  
  cat("Smaller than", x, "feet:", mean(split_data[[1]]$FGM), "(", nrow(split_data[[1]]), ")", '\n')
  cat("Larger than", x, "feet", mean(split_data[[2]]$FGM), "(", nrow(split_data[[2]]), ")", '\n')
}

test <- shot_data %>%
  filter(SHOT_DIST > 12 & SHOT_DIST <= 15)

x <- 0
while (x < 10) {
  get_split_fg(test, x)
  
  x <- x + 1
}
