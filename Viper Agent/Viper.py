import hlt
import logging

game = hlt.Game("Viper")
logging.info("Esse eh o meu mundo!")

while True:
    game_map = game.update_map()

    command_queue = []
   
    for ship in game_map.get_me().all_ships():
       
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        for planet in game_map.all_planets():

                if planet.calculate_distance_between( ship.closest_point_to(planet)) > 25.0:
                     ship.thrust(7, planet.calculate_angle_between( ship.closest_point_to(planet)))   

                if planet.is_owned() and planet.is_full():
                    continue
                else:
                    if len( planet.all_docked_ships() ) > 3:
                        continue
                    else:
                        ship.dock(planet)

            
                if ship.can_dock(planet):
                    command_queue.append(ship.dock(planet)) 
                else:
                    navigate_command = ship.navigate(
                            ship.closest_point_to(planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)
        
                    if navigate_command:
                        command_queue.append(navigate_command)
                break


    game.send_command_queue(command_queue)
 