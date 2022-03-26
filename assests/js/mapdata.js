var rayonName = "";

simplemaps_countrymap.hooks.click_state = function(id){

    rayonName = simplemaps_countrymap_mapdata.state_specific[id].name;

    console.log(rayonName)
    
   
    window.location.href="map.php?uid="+rayonName;
}



