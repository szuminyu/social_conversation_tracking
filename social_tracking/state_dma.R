options(stringsAsFactors = F)
options(scipens = 999)
library(tidyverse)
library(ggplot2)
library(readxl)
library(ggthemes)

setwd('/Users/Szu-MinYu/PycharmProjects/covid_19')

states = read_excel('state_dma.xlsx', sheet = 'state') %>% mutate(Name = stringr::str_to_lower(Name))
states_map = map_data('state')
states_map = states_map %>%
  left_join(states, by = c('region' = 'Name'))

png('states.png', width = 8, height = 5, units = 'in', res = 900)
ggplot(states_map, aes(long, lat, group = group)) + 
  geom_polygon(aes(fill = Score), color = 'white', size = 0.1) +
  scale_fill_distiller(direction = 1, name = 'Score')+
  coord_map()+
  theme_map()+
  #guides(fill =  guide_colorbar(title.position = "top", title.hjust = 0.5, nrow = 1, byrow = T))+
  theme(legend.position = 'None')
dev.off()


## dma 

#library(sp)
#library(rgdal)
#library(maptools)
#library(rgeos)
#library(ggalt)
#library(jsonlite)
#library(purrr)
#library(viridis)
#library(scales)



# DMA Chorepleth Map: need to have the json file stored in dma_heat_map folder
#get dma map
#neil = readOGR("nielsentopo.json", "nielsen_dma", stringsAsFactors=FALSE, 
#                verbose=FALSE)
# there are some techincal problems with the polygon that D3 glosses over
#transform and simplify
#neil_df = SpatialPolygonsDataFrame(rgeos::gSimplify(neil, tol = 0.0000001),data=neil@data)
#buffer:zero-width buffer cleans up many topology problems
#neil_df = gBuffer(neil_df, byid = T, width = 0) 
#0 means it's good polygon without any self-intersection
#sum(gIsValid(neil_df, byid = T)==F) 
#creat dframe for mapping
#neil_map = fortify(neil_df, region="id")


#dma = read_excel('state_dma.xlsx', sheet = 'dma')
#dma_coordinate = read_csv('dma_coordinates.csv') %>% select(dma, dma1)

#dma_map = dma %>%
#  left_join(dma_coordinate, by = c('DMA_name' = 'dma1')) %>%
#  mutate(dma = as.character(dma))
#dma_map = neil_map %>%
#  left_join(dma_map, by = c('id' = 'dma'))


#png('dma.png', width = 8, height = 5, units = 'in', res = 900)
#ggplot()+ 
#  geom_map(data=neil_map, map=neil_map,
#                    aes(x=long, y=lat, map_id= id),
#                    color="white", size=0.05, fill=NA)+ 
#  geom_map(data=dma_map, map=neil_map,
#                    aes(fill=`Posts_Count`, map_id=id),
#                    color="#bdbdbd", size=0.05)+
#  scale_fill_distiller(direction = 1, name = 'Posts Count', na.value = 'white')+
#  coord_proj(paste0("+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96",
#                    " +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs"))+ 
#  theme_map()+
#  guides(fill =  guide_colorbar(title.position = "top", title.hjust = 0.5, nrow = 1, byrow = T))+
#  theme(plot.title = element_text(hjust = 0.5, family = 'Calibri', size = 13),
#        legend.direction = "horizontal",
#        legend.justification="center" ,
#        legend.position = 'bottom',
#        legend.text = element_text(family = 'Calibri', size= 10),
#        legend.key.width=unit(2.7, "cm"),
#        legend.key.height = unit(0.2, 'cm'))
#dev.off()








