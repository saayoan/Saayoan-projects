# -*- coding: utf-8 -*-

@author: saayo
"""

# -*- coding: utf-8 -*-
"""
NBA Finals MVP Analyzer for Spyder
Analyzes championship teams and compares Finals MVP stats year by year
"""

# -*- coding: utf-8 -*-
"""
NBA Finals MVP Analyzer for Spyder
Analyzes championship teams and compares Finals MVP stats year by year
"""

from typing import Dict, List, Optional
from collections import defaultdict

# NBA Finals MVP Database (1969-2024)
# Format: Year: {"team": "Team Name", "mvp": "Player Name", "stats": {...}}
# Stats include: ppg, rpg, apg, fgp, 3pp (3-point %), spg (steals), bpg (blocks), tpg (turnovers), plus_minus
FINALS_MVP_DATABASE = {
    1969: {"team": "Boston Celtics", "mvp": "Jerry West", "stats": {"ppg": 37.9, "rpg": 4.7, "apg": 7.4, "fgp": 0.493, "3pp": 0.0, "spg": 2.1, "bpg": 0.3, "tpg": 3.8, "plus_minus": 8.2}},
    1970: {"team": "New York Knicks", "mvp": "Willis Reed", "stats": {"ppg": 23.7, "rpg": 13.8, "apg": 2.8, "fgp": 0.484}},
    1971: {"team": "Milwaukee Bucks", "mvp": "Kareem Abdul-Jabbar", "stats": {"ppg": 27.0, "rpg": 18.5, "apg": 2.8, "fgp": 0.605}},
    1972: {"team": "Los Angeles Lakers", "mvp": "Wilt Chamberlain", "stats": {"ppg": 19.4, "rpg": 23.2, "apg": 2.6, "fgp": 0.600}},
    1973: {"team": "New York Knicks", "mvp": "Willis Reed", "stats": {"ppg": 16.4, "rpg": 9.2, "apg": 2.6, "fgp": 0.478}},
    1974: {"team": "Boston Celtics", "mvp": "John Havlicek", "stats": {"ppg": 26.4, "rpg": 7.7, "apg": 2.7, "fgp": 0.448}},
    1975: {"team": "Golden State Warriors", "mvp": "Rick Barry", "stats": {"ppg": 29.5, "rpg": 4.0, "apg": 5.0, "fgp": 0.444}},
    1976: {"team": "Boston Celtics", "mvp": "Jo Jo White", "stats": {"ppg": 21.7, "rpg": 4.3, "apg": 5.8, "fgp": 0.444}},
    1977: {"team": "Portland Trail Blazers", "mvp": "Bill Walton", "stats": {"ppg": 18.5, "rpg": 19.0, "apg": 5.2, "fgp": 0.508}},
    1978: {"team": "Washington Bullets", "mvp": "Wes Unseld", "stats": {"ppg": 9.0, "rpg": 11.7, "apg": 3.9, "fgp": 0.500}},
    1979: {"team": "Seattle SuperSonics", "mvp": "Dennis Johnson", "stats": {"ppg": 22.6, "rpg": 6.0, "apg": 6.0, "fgp": 0.456}},
    1980: {"team": "Los Angeles Lakers", "mvp": "Magic Johnson", "stats": {"ppg": 21.5, "rpg": 11.2, "apg": 8.7, "fgp": 0.573}},
    1981: {"team": "Boston Celtics", "mvp": "Cedric Maxwell", "stats": {"ppg": 17.7, "rpg": 9.5, "apg": 2.8, "fgp": 0.568}},
    1982: {"team": "Los Angeles Lakers", "mvp": "Magic Johnson", "stats": {"ppg": 16.2, "rpg": 10.8, "apg": 8.0, "fgp": 0.533}},
    1983: {"team": "Philadelphia 76ers", "mvp": "Moses Malone", "stats": {"ppg": 25.8, "rpg": 18.0, "apg": 1.5, "fgp": 0.503}},
    1984: {"team": "Boston Celtics", "mvp": "Larry Bird", "stats": {"ppg": 27.4, "rpg": 14.0, "apg": 3.6, "fgp": 0.484}},
    1985: {"team": "Los Angeles Lakers", "mvp": "Kareem Abdul-Jabbar", "stats": {"ppg": 25.7, "rpg": 9.0, "apg": 5.2, "fgp": 0.600}},
    1986: {"team": "Boston Celtics", "mvp": "Larry Bird", "stats": {"ppg": 24.0, "rpg": 9.7, "apg": 9.5, "fgp": 0.482}},
    1987: {"team": "Los Angeles Lakers", "mvp": "Magic Johnson", "stats": {"ppg": 26.2, "rpg": 8.0, "apg": 13.0, "fgp": 0.541}},
    1988: {"team": "Los Angeles Lakers", "mvp": "James Worthy", "stats": {"ppg": 22.0, "rpg": 7.4, "apg": 4.4, "fgp": 0.490}},
    1989: {"team": "Detroit Pistons", "mvp": "Joe Dumars", "stats": {"ppg": 27.3, "rpg": 1.8, "apg": 6.0, "fgp": 0.576}},
    1990: {"team": "Detroit Pistons", "mvp": "Isiah Thomas", "stats": {"ppg": 27.6, "rpg": 5.2, "apg": 7.0, "fgp": 0.545}},
    1991: {"team": "Chicago Bulls", "mvp": "Michael Jordan", "stats": {"ppg": 31.2, "rpg": 6.6, "apg": 11.4, "fgp": 0.558, "3pp": 0.500, "spg": 2.8, "bpg": 1.4, "tpg": 2.5, "plus_minus": 15.2}},
    1992: {"team": "Chicago Bulls", "mvp": "Michael Jordan", "stats": {"ppg": 35.8, "rpg": 4.8, "apg": 6.5, "fgp": 0.526, "3pp": 0.429, "spg": 1.7, "bpg": 0.3, "tpg": 2.8, "plus_minus": 12.5}},
    1993: {"team": "Chicago Bulls", "mvp": "Michael Jordan", "stats": {"ppg": 41.0, "rpg": 8.5, "apg": 6.3, "fgp": 0.508, "3pp": 0.400, "spg": 1.7, "bpg": 0.7, "tpg": 2.3, "plus_minus": 16.0}},
    1994: {"team": "Houston Rockets", "mvp": "Hakeem Olajuwon", "stats": {"ppg": 26.9, "rpg": 9.1, "apg": 3.6, "fgp": 0.500}},
    1995: {"team": "Houston Rockets", "mvp": "Hakeem Olajuwon", "stats": {"ppg": 32.8, "rpg": 11.5, "apg": 5.5, "fgp": 0.483}},
    1996: {"team": "Chicago Bulls", "mvp": "Michael Jordan", "stats": {"ppg": 27.3, "rpg": 5.3, "apg": 4.2, "fgp": 0.415}},
    1997: {"team": "Chicago Bulls", "mvp": "Michael Jordan", "stats": {"ppg": 32.3, "rpg": 7.0, "apg": 6.0, "fgp": 0.456}},
    1998: {"team": "Chicago Bulls", "mvp": "Michael Jordan", "stats": {"ppg": 33.5, "rpg": 4.0, "apg": 2.3, "fgp": 0.427}},
    1999: {"team": "San Antonio Spurs", "mvp": "Tim Duncan", "stats": {"ppg": 27.4, "rpg": 14.0, "apg": 2.4, "fgp": 0.539}},
    2000: {"team": "Los Angeles Lakers", "mvp": "Shaquille O'Neal", "stats": {"ppg": 38.0, "rpg": 16.7, "apg": 2.3, "fgp": 0.611}},
    2001: {"team": "Los Angeles Lakers", "mvp": "Shaquille O'Neal", "stats": {"ppg": 33.0, "rpg": 15.8, "apg": 4.8, "fgp": 0.573}},
    2002: {"team": "Los Angeles Lakers", "mvp": "Shaquille O'Neal", "stats": {"ppg": 36.3, "rpg": 12.3, "apg": 3.8, "fgp": 0.595}},
    2003: {"team": "San Antonio Spurs", "mvp": "Tim Duncan", "stats": {"ppg": 24.2, "rpg": 17.0, "apg": 5.3, "fgp": 0.494}},
    2004: {"team": "Detroit Pistons", "mvp": "Chauncey Billups", "stats": {"ppg": 21.0, "rpg": 3.2, "apg": 5.2, "fgp": 0.506}},
    2005: {"team": "San Antonio Spurs", "mvp": "Tim Duncan", "stats": {"ppg": 20.6, "rpg": 14.1, "apg": 2.1, "fgp": 0.417}},
    2006: {"team": "Miami Heat", "mvp": "Dwyane Wade", "stats": {"ppg": 34.7, "rpg": 7.8, "apg": 3.8, "fgp": 0.469}},
    2007: {"team": "San Antonio Spurs", "mvp": "Tony Parker", "stats": {"ppg": 24.5, "rpg": 5.0, "apg": 3.3, "fgp": 0.568}},
    2008: {"team": "Boston Celtics", "mvp": "Paul Pierce", "stats": {"ppg": 21.8, "rpg": 4.5, "apg": 6.3, "fgp": 0.435}},
    2009: {"team": "Los Angeles Lakers", "mvp": "Kobe Bryant", "stats": {"ppg": 32.4, "rpg": 5.6, "apg": 7.4, "fgp": 0.430}},
    2010: {"team": "Los Angeles Lakers", "mvp": "Kobe Bryant", "stats": {"ppg": 28.6, "rpg": 8.0, "apg": 3.9, "fgp": 0.405}},
    2011: {"team": "Dallas Mavericks", "mvp": "Dirk Nowitzki", "stats": {"ppg": 26.0, "rpg": 9.7, "apg": 2.0, "fgp": 0.416}},
    2012: {"team": "Miami Heat", "mvp": "LeBron James", "stats": {"ppg": 28.6, "rpg": 10.2, "apg": 7.4, "fgp": 0.472}},
    2013: {"team": "Miami Heat", "mvp": "LeBron James", "stats": {"ppg": 25.3, "rpg": 10.9, "apg": 7.0, "fgp": 0.447}},
    2014: {"team": "San Antonio Spurs", "mvp": "Kawhi Leonard", "stats": {"ppg": 17.8, "rpg": 6.4, "apg": 2.0, "fgp": 0.612}},
    2015: {"team": "Golden State Warriors", "mvp": "Andre Iguodala", "stats": {"ppg": 16.3, "rpg": 5.8, "apg": 4.0, "fgp": 0.521}},
    2016: {"team": "Cleveland Cavaliers", "mvp": "LeBron James", "stats": {"ppg": 29.7, "rpg": 11.3, "apg": 8.9, "fgp": 0.490}},
    2017: {"team": "Golden State Warriors", "mvp": "Kevin Durant", "stats": {"ppg": 35.2, "rpg": 8.2, "apg": 5.4, "fgp": 0.556}},
    2018: {"team": "Golden State Warriors", "mvp": "Kevin Durant", "stats": {"ppg": 28.8, "rpg": 10.8, "apg": 7.5, "fgp": 0.526}},
    2019: {"team": "Toronto Raptors", "mvp": "Kawhi Leonard", "stats": {"ppg": 28.5, "rpg": 9.8, "apg": 4.2, "fgp": 0.436}},
    2020: {"team": "Los Angeles Lakers", "mvp": "LeBron James", "stats": {"ppg": 29.8, "rpg": 11.8, "apg": 8.5, "fgp": 0.591}},
    2021: {"team": "Milwaukee Bucks", "mvp": "Giannis Antetokounmpo", "stats": {"ppg": 35.2, "rpg": 13.2, "apg": 5.0, "fgp": 0.618}},
    2022: {"team": "Golden State Warriors", "mvp": "Stephen Curry", "stats": {"ppg": 31.2, "rpg": 6.0, "apg": 5.0, "fgp": 0.483}},
    2023: {"team": "Denver Nuggets", "mvp": "Nikola Jokic", "stats": {"ppg": 30.2, "rpg": 14.0, "apg": 7.2, "fgp": 0.584}},
    2024: {"team": "Boston Celtics", "mvp": "Jayson Tatum", "stats": {"ppg": 20.8, "rpg": 7.2, "apg": 7.2, "fgp": 0.367}},
}

# Championship Team Rosters (key players from each championship team)
# Format: Year: [list of player names on the championship roster]
CHAMPIONSHIP_ROSTERS = {
    1969: ["Bill Russell", "Sam Jones", "John Havlicek", "Bailey Howell", "Larry Siegfried", "Don Nelson"],
    1970: ["Willis Reed", "Walt Frazier", "Dave DeBusschere", "Bill Bradley", "Dick Barnett", "Cazzie Russell"],
    1971: ["Kareem Abdul-Jabbar", "Oscar Robertson", "Bob Dandridge", "Jon McGlocklin", "Greg Smith"],
    1972: ["Wilt Chamberlain", "Jerry West", "Gail Goodrich", "Jim McMillian", "Happy Hairston"],
    1973: ["Willis Reed", "Walt Frazier", "Dave DeBusschere", "Bill Bradley", "Earl Monroe", "Jerry Lucas"],
    1974: ["John Havlicek", "Dave Cowens", "Jo Jo White", "Don Nelson", "Paul Silas", "Don Chaney"],
    1975: ["Rick Barry", "Jamaal Wilkes", "Phil Smith", "Clifford Ray", "Butch Beard"],
    1976: ["John Havlicek", "Dave Cowens", "Jo Jo White", "Charlie Scott", "Paul Silas"],
    1977: ["Bill Walton", "Maurice Lucas", "Lionel Hollins", "Bob Gross", "Dave Twardzik"],
    1978: ["Wes Unseld", "Elvin Hayes", "Bob Dandridge", "Kevin Grevey", "Mitch Kupchak"],
    1979: ["Dennis Johnson", "Gus Williams", "Jack Sikma", "John Johnson", "Fred Brown"],
    1980: ["Magic Johnson", "Kareem Abdul-Jabbar", "Jamaal Wilkes", "Norm Nixon", "Michael Cooper"],
    1981: ["Larry Bird", "Cedric Maxwell", "Robert Parish", "Nate Archibald", "Kevin McHale"],
    1982: ["Magic Johnson", "Kareem Abdul-Jabbar", "Jamaal Wilkes", "Norm Nixon", "Michael Cooper"],
    1983: ["Moses Malone", "Julius Erving", "Andrew Toney", "Maurice Cheeks", "Bobby Jones"],
    1984: ["Larry Bird", "Kevin McHale", "Robert Parish", "Dennis Johnson", "Gerald Henderson"],
    1985: ["Magic Johnson", "Kareem Abdul-Jabbar", "James Worthy", "Byron Scott", "Michael Cooper"],
    1986: ["Larry Bird", "Kevin McHale", "Robert Parish", "Dennis Johnson", "Danny Ainge"],
    1987: ["Magic Johnson", "Kareem Abdul-Jabbar", "James Worthy", "Byron Scott", "A.C. Green"],
    1988: ["Magic Johnson", "James Worthy", "Kareem Abdul-Jabbar", "Byron Scott", "A.C. Green"],
    1989: ["Isiah Thomas", "Joe Dumars", "Bill Laimbeer", "Mark Aguirre", "Dennis Rodman"],
    1990: ["Isiah Thomas", "Joe Dumars", "Bill Laimbeer", "Mark Aguirre", "Dennis Rodman"],
    1991: ["Michael Jordan", "Scottie Pippen", "Horace Grant", "John Paxson", "Bill Cartwright"],
    1992: ["Michael Jordan", "Scottie Pippen", "Horace Grant", "B.J. Armstrong", "Bill Cartwright"],
    1993: ["Michael Jordan", "Scottie Pippen", "Horace Grant", "B.J. Armstrong", "Bill Cartwright"],
    1994: ["Hakeem Olajuwon", "Vernon Maxwell", "Kenny Smith", "Otis Thorpe", "Robert Horry"],
    1995: ["Hakeem Olajuwon", "Clyde Drexler", "Kenny Smith", "Robert Horry", "Sam Cassell"],
    1996: ["Michael Jordan", "Scottie Pippen", "Dennis Rodman", "Toni Kukoc", "Ron Harper"],
    1997: ["Michael Jordan", "Scottie Pippen", "Dennis Rodman", "Toni Kukoc", "Ron Harper"],
    1998: ["Michael Jordan", "Scottie Pippen", "Dennis Rodman", "Toni Kukoc", "Ron Harper"],
    1999: ["Tim Duncan", "David Robinson", "Sean Elliott", "Avery Johnson", "Mario Elie"],
    2000: ["Shaquille O'Neal", "Kobe Bryant", "Glen Rice", "Ron Harper", "Robert Horry"],
    2001: ["Shaquille O'Neal", "Kobe Bryant", "Derek Fisher", "Rick Fox", "Robert Horry"],
    2002: ["Shaquille O'Neal", "Kobe Bryant", "Derek Fisher", "Rick Fox", "Robert Horry"],
    2003: ["Tim Duncan", "Tony Parker", "Manu Ginobili", "David Robinson", "Stephen Jackson"],
    2004: ["Chauncey Billups", "Ben Wallace", "Rasheed Wallace", "Richard Hamilton", "Tayshaun Prince"],
    2005: ["Tim Duncan", "Tony Parker", "Manu Ginobili", "Bruce Bowen", "Robert Horry"],
    2006: ["Dwyane Wade", "Shaquille O'Neal", "Udonis Haslem", "Antoine Walker", "Jason Williams"],
    2007: ["Tim Duncan", "Tony Parker", "Manu Ginobili", "Bruce Bowen", "Fabricio Oberto"],
    2008: ["Paul Pierce", "Kevin Garnett", "Ray Allen", "Rajon Rondo", "Kendrick Perkins"],
    2009: ["Kobe Bryant", "Pau Gasol", "Lamar Odom", "Trevor Ariza", "Derek Fisher"],
    2010: ["Kobe Bryant", "Pau Gasol", "Ron Artest", "Lamar Odom", "Derek Fisher"],
    2011: ["Dirk Nowitzki", "Jason Terry", "Jason Kidd", "Shawn Marion", "Tyson Chandler"],
    2012: ["LeBron James", "Dwyane Wade", "Chris Bosh", "Mario Chalmers", "Shane Battier"],
    2013: ["LeBron James", "Dwyane Wade", "Chris Bosh", "Ray Allen", "Mario Chalmers"],
    2014: ["Kawhi Leonard", "Tim Duncan", "Tony Parker", "Manu Ginobili", "Danny Green"],
    2015: ["Stephen Curry", "Klay Thompson", "Draymond Green", "Andre Iguodala", "Harrison Barnes"],
    2016: ["LeBron James", "Kyrie Irving", "Kevin Love", "Tristan Thompson", "J.R. Smith"],
    2017: ["Kevin Durant", "Stephen Curry", "Klay Thompson", "Draymond Green", "Andre Iguodala"],
    2018: ["Kevin Durant", "Stephen Curry", "Klay Thompson", "Draymond Green", "Andre Iguodala"],
    2019: ["Kawhi Leonard", "Kyle Lowry", "Pascal Siakam", "Marc Gasol", "Fred VanVleet"],
    2020: ["LeBron James", "Anthony Davis", "Rajon Rondo", "Danny Green", "Kyle Kuzma"],
    2021: ["Giannis Antetokounmpo", "Khris Middleton", "Jrue Holiday", "Brook Lopez", "Bobby Portis"],
    2022: ["Stephen Curry", "Klay Thompson", "Draymond Green", "Andrew Wiggins", "Jordan Poole"],
    2023: ["Nikola Jokic", "Jamal Murray", "Michael Porter Jr.", "Aaron Gordon", "Kentavious Caldwell-Pope"],
    2024: ["Jayson Tatum", "Jaylen Brown", "Kristaps Porzingis", "Jrue Holiday", "Derrick White"],
}

# Player Finals Stats Database (for all championship players, not just MVPs)
# Format: (Year, Player Name): stats
PLAYER_FINALS_STATS = {}
# Initialize with Finals MVP stats
for year, data in FINALS_MVP_DATABASE.items():
    mvp_name = data["mvp"]
    PLAYER_FINALS_STATS[(year, mvp_name)] = data["stats"]

# Add key non-MVP players' Finals stats (representative data)
# Note: In a real implementation, you'd have complete stats for all players
# For now, we'll use estimated stats based on typical roles
KEY_PLAYER_STATS = {
    # 1991 Bulls
    (1991, "Scottie Pippen"): {"ppg": 20.8, "rpg": 9.4, "apg": 6.6, "fgp": 0.454, "3pp": 0.200, "spg": 2.4, "bpg": 1.0, "tpg": 2.6, "plus_minus": 12.8},
    (1991, "Horace Grant"): {"ppg": 11.2, "rpg": 8.8, "apg": 2.2, "fgp": 0.500, "3pp": 0.0, "spg": 0.8, "bpg": 0.6, "tpg": 1.4, "plus_minus": 8.2},
    # 1992 Bulls
    (1992, "Scottie Pippen"): {"ppg": 20.8, "rpg": 8.3, "apg": 7.7, "fgp": 0.481},
    # 1993 Bulls
    (1993, "Scottie Pippen"): {"ppg": 21.2, "rpg": 9.2, "apg": 7.7, "fgp": 0.439},
    # 1996 Bulls
    (1996, "Scottie Pippen"): {"ppg": 15.7, "rpg": 6.8, "apg": 5.3, "fgp": 0.343},
    (1996, "Dennis Rodman"): {"ppg": 7.5, "rpg": 14.7, "apg": 2.5, "fgp": 0.480},
    # 1997 Bulls
    (1997, "Scottie Pippen"): {"ppg": 20.0, "rpg": 8.3, "apg": 3.5, "fgp": 0.420},
    (1997, "Dennis Rodman"): {"ppg": 2.3, "rpg": 11.8, "apg": 1.5, "fgp": 0.313},
    # 1998 Bulls
    (1998, "Scottie Pippen"): {"ppg": 15.7, "rpg": 6.8, "apg": 4.8, "fgp": 0.410},
    (1998, "Dennis Rodman"): {"ppg": 3.3, "rpg": 8.3, "apg": 1.0, "fgp": 0.333},
    # 2000 Lakers
    (2000, "Kobe Bryant"): {"ppg": 15.6, "rpg": 4.6, "apg": 4.2, "fgp": 0.367},
    # 2001 Lakers
    (2001, "Kobe Bryant"): {"ppg": 24.6, "rpg": 7.8, "apg": 5.8, "fgp": 0.415},
    # 2002 Lakers
    (2002, "Kobe Bryant"): {"ppg": 26.8, "rpg": 5.8, "apg": 5.3, "fgp": 0.514},
    # 2008 Celtics
    (2008, "Kevin Garnett"): {"ppg": 18.2, "rpg": 13.0, "apg": 3.0, "fgp": 0.429},
    (2008, "Ray Allen"): {"ppg": 20.3, "rpg": 5.0, "apg": 2.5, "fgp": 0.507},
    (2008, "Rajon Rondo"): {"ppg": 9.3, "rpg": 3.6, "apg": 6.7, "fgp": 0.379},
    # 2009 Lakers
    (2009, "Pau Gasol"): {"ppg": 18.6, "rpg": 9.2, "apg": 2.2, "fgp": 0.600},
    # 2010 Lakers
    (2010, "Pau Gasol"): {"ppg": 18.6, "rpg": 11.6, "apg": 3.7, "fgp": 0.478},
    # 2012 Heat
    (2012, "Dwyane Wade"): {"ppg": 22.6, "rpg": 6.0, "apg": 5.2, "fgp": 0.435, "3pp": 0.273, "spg": 1.4, "bpg": 1.2, "tpg": 2.6, "plus_minus": 7.8},
    (2012, "Chris Bosh"): {"ppg": 14.6, "rpg": 9.4, "apg": 0.2, "fgp": 0.455, "3pp": 0.538, "spg": 0.6, "bpg": 1.2, "tpg": 1.0, "plus_minus": 4.2},
    # 2013 Heat
    (2013, "Dwyane Wade"): {"ppg": 19.6, "rpg": 4.0, "apg": 4.6, "fgp": 0.477, "3pp": 0.250, "spg": 1.9, "bpg": 0.9, "tpg": 2.1, "plus_minus": 6.4},
    (2013, "Chris Bosh"): {"ppg": 11.9, "rpg": 8.9, "apg": 0.6, "fgp": 0.478, "3pp": 0.400, "spg": 0.4, "bpg": 0.6, "tpg": 1.1, "plus_minus": 3.8},
    # 2014 Spurs
    (2014, "Tim Duncan"): {"ppg": 15.4, "rpg": 10.0, "apg": 2.0, "fgp": 0.568},
    (2014, "Tony Parker"): {"ppg": 18.0, "rpg": 0.6, "apg": 4.6, "fgp": 0.477},
    # 2015 Warriors
    (2015, "Stephen Curry"): {"ppg": 26.0, "rpg": 5.2, "apg": 6.3, "fgp": 0.443, "3pp": 0.385, "spg": 1.8, "bpg": 0.2, "tpg": 4.7, "plus_minus": 4.5},
    (2015, "Klay Thompson"): {"ppg": 15.8, "rpg": 4.3, "apg": 1.2, "fgp": 0.404, "3pp": 0.429, "spg": 0.8, "bpg": 0.2, "tpg": 1.5, "plus_minus": 3.2},
    (2015, "Draymond Green"): {"ppg": 13.0, "rpg": 10.1, "apg": 5.5, "fgp": 0.385, "3pp": 0.250, "spg": 1.5, "bpg": 1.2, "tpg": 2.3, "plus_minus": 5.8},
    # 2016 Cavaliers
    (2016, "Kyrie Irving"): {"ppg": 27.1, "rpg": 3.9, "apg": 3.9, "fgp": 0.468, "3pp": 0.405, "spg": 2.1, "bpg": 0.1, "tpg": 2.6, "plus_minus": 3.5},
    (2016, "Kevin Love"): {"ppg": 8.5, "rpg": 6.8, "apg": 1.3, "fgp": 0.365, "3pp": 0.263, "spg": 0.5, "bpg": 0.3, "tpg": 1.3, "plus_minus": 1.2},
    # 2017 Warriors
    (2017, "Stephen Curry"): {"ppg": 26.8, "rpg": 8.0, "apg": 9.4, "fgp": 0.439},
    (2017, "Klay Thompson"): {"ppg": 16.4, "rpg": 4.8, "apg": 2.2, "fgp": 0.426},
    # 2018 Warriors
    (2018, "Stephen Curry"): {"ppg": 27.5, "rpg": 6.0, "apg": 6.8, "fgp": 0.402},
    (2018, "Klay Thompson"): {"ppg": 16.0, "rpg": 3.8, "apg": 2.0, "fgp": 0.425},
    # 2019 Raptors
    (2019, "Kyle Lowry"): {"ppg": 16.2, "rpg": 4.0, "apg": 7.2, "fgp": 0.425},
    (2019, "Pascal Siakam"): {"ppg": 19.8, "rpg": 7.5, "apg": 3.7, "fgp": 0.506},
    # 2020 Lakers
    (2020, "Anthony Davis"): {"ppg": 25.0, "rpg": 10.7, "apg": 3.2, "fgp": 0.571},
    # 2021 Bucks
    (2021, "Khris Middleton"): {"ppg": 24.0, "rpg": 6.3, "apg": 5.3, "fgp": 0.435},
    (2021, "Jrue Holiday"): {"ppg": 16.7, "rpg": 6.2, "apg": 9.3, "fgp": 0.361},
    # 2022 Warriors
    (2022, "Klay Thompson"): {"ppg": 17.0, "rpg": 2.8, "apg": 2.0, "fgp": 0.355},
    (2022, "Draymond Green"): {"ppg": 6.2, "rpg": 8.0, "apg": 6.2, "fgp": 0.333},
    (2022, "Andrew Wiggins"): {"ppg": 18.3, "rpg": 6.3, "apg": 1.7, "fgp": 0.456},
    # 2023 Nuggets
    (2023, "Jamal Murray"): {"ppg": 21.4, "rpg": 6.2, "apg": 10.0, "fgp": 0.454},
    (2023, "Michael Porter Jr."): {"ppg": 13.4, "rpg": 8.4, "apg": 1.2, "fgp": 0.421},
    # 2024 Celtics
    (2024, "Jaylen Brown"): {"ppg": 20.8, "rpg": 5.4, "apg": 5.0, "fgp": 0.444},
    (2024, "Jrue Holiday"): {"ppg": 14.4, "rpg": 7.4, "apg": 3.6, "fgp": 0.500},
}

# Merge key player stats into main database
PLAYER_FINALS_STATS.update(KEY_PLAYER_STATS)

# Function to add default advanced stats to entries missing them
def add_default_advanced_stats(stats_dict: Dict) -> Dict:
    """Add default advanced stats to entries that don't have them"""
    defaults = {
        "3pp": 0.0,  # 3-point percentage (0.0 for pre-3pt era or non-shooters)
        "spg": 1.5,  # steals per game
        "bpg": 0.5,  # blocks per game
        "tpg": 2.5,  # turnovers per game
        "plus_minus": 5.0  # plus/minus per game
    }
    for key, default_value in defaults.items():
        if key not in stats_dict:
            stats_dict[key] = default_value
    return stats_dict

# Update all database entries to include advanced stats
for year, data in FINALS_MVP_DATABASE.items():
    data["stats"] = add_default_advanced_stats(data["stats"])

# Update key modern entries with realistic advanced stats
modern_updates = {
    2000: {"3pp": 0.0, "spg": 0.5, "bpg": 3.0, "tpg": 3.2, "plus_minus": 18.5},
    2001: {"3pp": 0.0, "spg": 0.4, "bpg": 2.4, "tpg": 3.5, "plus_minus": 16.8},
    2002: {"3pp": 0.0, "spg": 0.5, "bpg": 2.8, "tpg": 3.0, "plus_minus": 17.2},
    2006: {"3pp": 0.273, "spg": 2.7, "bpg": 1.0, "tpg": 3.5, "plus_minus": 12.3},
    2008: {"3pp": 0.393, "spg": 1.2, "bpg": 0.2, "tpg": 3.0, "plus_minus": 8.5},
    2009: {"3pp": 0.360, "spg": 1.4, "bpg": 0.2, "tpg": 2.6, "plus_minus": 7.8},
    2010: {"3pp": 0.316, "spg": 0.7, "bpg": 0.4, "tpg": 3.4, "plus_minus": 6.2},
    2011: {"3pp": 0.368, "spg": 0.7, "bpg": 0.7, "tpg": 2.0, "plus_minus": 9.8},
    2012: {"3pp": 0.188, "spg": 1.6, "bpg": 0.4, "tpg": 3.8, "plus_minus": 10.2},
    2013: {"3pp": 0.353, "spg": 1.9, "bpg": 0.9, "tpg": 3.0, "plus_minus": 8.8},
    2014: {"3pp": 0.577, "spg": 2.0, "bpg": 1.2, "tpg": 1.0, "plus_minus": 14.3},
    2015: {"3pp": 0.400, "spg": 1.3, "bpg": 0.3, "tpg": 1.3, "plus_minus": 4.2},
    2016: {"3pp": 0.371, "spg": 2.6, "bpg": 2.3, "tpg": 4.4, "plus_minus": 5.7},
    2017: {"3pp": 0.474, "spg": 1.0, "bpg": 1.6, "tpg": 2.2, "plus_minus": 11.5},
    2018: {"3pp": 0.409, "spg": 0.8, "bpg": 2.3, "tpg": 2.5, "plus_minus": 10.2},
    2019: {"3pp": 0.359, "spg": 2.0, "bpg": 0.5, "tpg": 2.3, "plus_minus": 8.0},
    2020: {"3pp": 0.415, "spg": 1.8, "bpg": 0.5, "tpg": 3.5, "plus_minus": 7.8},
    2021: {"3pp": 0.200, "spg": 1.2, "bpg": 1.8, "tpg": 3.7, "plus_minus": 9.5},
    2022: {"3pp": 0.437, "spg": 2.0, "bpg": 0.2, "tpg": 2.6, "plus_minus": 5.4},
    2023: {"3pp": 0.421, "spg": 1.4, "bpg": 0.4, "tpg": 3.2, "plus_minus": 8.1},
    2024: {"3pp": 0.313, "spg": 1.0, "bpg": 0.2, "tpg": 2.8, "plus_minus": 4.2},
}

for year, adv_stats in modern_updates.items():
    if year in FINALS_MVP_DATABASE:
        FINALS_MVP_DATABASE[year]["stats"].update(adv_stats)

# Era adjustments for fair comparison (pace, competition, rules)
ERA_ADJUSTMENTS = {
    "1960s": {"pace_multiplier": 1.15, "competition_multiplier": 0.95},
    "1970s": {"pace_multiplier": 1.10, "competition_multiplier": 0.97},
    "1980s": {"pace_multiplier": 1.05, "competition_multiplier": 1.00},
    "1990s": {"pace_multiplier": 1.00, "competition_multiplier": 1.02},
    "2000s": {"pace_multiplier": 0.98, "competition_multiplier": 1.03},
    "2010s": {"pace_multiplier": 0.95, "competition_multiplier": 1.05},
    "2020s": {"pace_multiplier": 0.93, "competition_multiplier": 1.08},
}


def get_era(year: int) -> str:
    """Determine the era for a given year"""
    if year < 1970:
        return "1960s"
    elif year < 1980:
        return "1970s"
    elif year < 1990:
        return "1980s"
    elif year < 2000:
        return "1990s"
    elif year < 2010:
        return "2000s"
    elif year < 2020:
        return "2010s"
    else:
        return "2020s"


def get_player_years(player_name: str) -> List[int]:
    """Get all years a player won Finals MVP"""
    years = []
    for year, data in FINALS_MVP_DATABASE.items():
        if data["mvp"].lower() == player_name.lower():
            years.append(year)
    return sorted(years)


def is_player_on_championship_roster(player_name: str) -> bool:
    """Check if a player was on any championship roster"""
    player_name_lower = player_name.lower()
    for year, roster in CHAMPIONSHIP_ROSTERS.items():
        for roster_player in roster:
            if roster_player.lower() == player_name_lower:
                return True
    return False


def get_championship_years_for_player(player_name: str) -> List[int]:
    """Get all years a player was on a championship roster"""
    years = []
    player_name_lower = player_name.lower()
    for year, roster in CHAMPIONSHIP_ROSTERS.items():
        for roster_player in roster:
            if roster_player.lower() == player_name_lower:
                years.append(year)
                break
    return sorted(years)


def get_player_finals_stats(player_name: str, year: int) -> Optional[Dict]:
    """Get Finals stats for a player in a specific year"""
    player_name_lower = player_name.lower()
    # Try exact match first
    for (y, name), stats in PLAYER_FINALS_STATS.items():
        if y == year and name.lower() == player_name_lower:
            return add_default_advanced_stats(stats.copy())
    # If not found, check if player was on roster and use estimated stats
    if year in CHAMPIONSHIP_ROSTERS:
        roster = CHAMPIONSHIP_ROSTERS[year]
        for roster_player in roster:
            if roster_player.lower() == player_name_lower:
                # Return estimated stats based on role (simplified)
                # In a real system, you'd have complete stats
                base_stats = {"ppg": 12.0, "rpg": 5.0, "apg": 3.0, "fgp": 0.450}
                return add_default_advanced_stats(base_stats)
    return None


def get_all_players() -> List[str]:
    """Get list of all Finals MVP winners"""
    players = set()
    for data in FINALS_MVP_DATABASE.values():
        players.add(data["mvp"])
    return sorted(list(players))


def analyze_player(player_name: str) -> Optional[Dict]:
    """Analyze a specific championship player year by year (works for any player on championship roster)"""
    # First check if player was on any championship roster
    if not is_player_on_championship_roster(player_name):
        return None
    
    # Get all years player was on championship roster
    player_years = get_championship_years_for_player(player_name)
    
    if not player_years:
        return None
    
    analysis = {
        "name": player_name,
        "years": player_years,
        "championships": len(player_years),
        "yearly_stats": [],
        "career_averages": {"ppg": 0, "rpg": 0, "apg": 0, "fgp": 0, "3pp": 0, "spg": 0, "bpg": 0, "tpg": 0, "plus_minus": 0},
        "best_year": None,
        "best_stats": None
    }
    
    total_ppg = 0
    total_rpg = 0
    total_apg = 0
    total_fgp = 0
    total_3pp = 0
    total_spg = 0
    total_bpg = 0
    total_tpg = 0
    total_plus_minus = 0
    best_ppg = 0
    
    for year in player_years:
        # Get team name
        team_name = FINALS_MVP_DATABASE[year]["team"]
        
        # Get player's Finals stats for this year
        stats = get_player_finals_stats(player_name, year)
        
        if not stats:
            # Fallback: use Finals MVP stats if player was the MVP
            if FINALS_MVP_DATABASE[year]["mvp"].lower() == player_name.lower():
                stats = FINALS_MVP_DATABASE[year]["stats"].copy()
            else:
                # Use estimated stats
                stats = {"ppg": 12.0, "rpg": 5.0, "apg": 3.0, "fgp": 0.450}
        
        # Ensure all advanced stats are present
        stats = add_default_advanced_stats(stats.copy())
        
        era = get_era(year)
        
        year_data = {
            "year": year,
            "team": team_name,
            "stats": stats,
            "era": era,
            "adjusted_ppg": stats["ppg"] * ERA_ADJUSTMENTS[era]["pace_multiplier"]
        }
        
        analysis["yearly_stats"].append(year_data)
        
        total_ppg += stats["ppg"]
        total_rpg += stats["rpg"]
        total_apg += stats["apg"]
        total_fgp += stats["fgp"]
        total_3pp += stats.get("3pp", 0.0)
        total_spg += stats.get("spg", 0.0)
        total_bpg += stats.get("bpg", 0.0)
        total_tpg += stats.get("tpg", 0.0)
        total_plus_minus += stats.get("plus_minus", 0.0)
        
        if stats["ppg"] > best_ppg:
            best_ppg = stats["ppg"]
            analysis["best_year"] = year
            analysis["best_stats"] = stats
    
    # Calculate career averages
    num_years = len(player_years)
    analysis["career_averages"]["ppg"] = total_ppg / num_years
    analysis["career_averages"]["rpg"] = total_rpg / num_years
    analysis["career_averages"]["apg"] = total_apg / num_years
    analysis["career_averages"]["fgp"] = total_fgp / num_years
    analysis["career_averages"]["3pp"] = total_3pp / num_years
    analysis["career_averages"]["spg"] = total_spg / num_years
    analysis["career_averages"]["bpg"] = total_bpg / num_years
    analysis["career_averages"]["tpg"] = total_tpg / num_years
    analysis["career_averages"]["plus_minus"] = total_plus_minus / num_years
    
    return analysis


def compare_players(player1_name: str, player2_name: str) -> Dict:
    """Compare any two players from championship rosters"""
    # Check if both players were on championship rosters
    p1_on_roster = is_player_on_championship_roster(player1_name)
    p2_on_roster = is_player_on_championship_roster(player2_name)
    
    if not p1_on_roster and not p2_on_roster:
        return {"error": f"ERROR: Neither '{player1_name}' nor '{player2_name}' were on any championship roster."}
    elif not p1_on_roster:
        return {"error": f"ERROR: '{player1_name}' was not on any championship roster."}
    elif not p2_on_roster:
        return {"error": f"ERROR: '{player2_name}' was not on any championship roster."}
    
    p1 = analyze_player(player1_name)
    p2 = analyze_player(player2_name)
    
    if not p1 or not p2:
        return {"error": "ERROR: Could not retrieve player data. Please check the names."}
    
    comparison = {
        "player1": p1,
        "player2": p2,
        "head_to_head": {
            "championships": {
                "player1": p1["championships"],
                "player2": p2["championships"],
                "winner": player1_name if p1["championships"] > p2["championships"] else player2_name if p2["championships"] > p1["championships"] else "Tie"
            },
            "ppg": {
                "player1": p1["career_averages"]["ppg"],
                "player2": p2["career_averages"]["ppg"],
                "winner": player1_name if p1["career_averages"]["ppg"] > p2["career_averages"]["ppg"] else player2_name
            },
            "rpg": {
                "player1": p1["career_averages"]["rpg"],
                "player2": p2["career_averages"]["rpg"],
                "winner": player1_name if p1["career_averages"]["rpg"] > p2["career_averages"]["rpg"] else player2_name
            },
            "apg": {
                "player1": p1["career_averages"]["apg"],
                "player2": p2["career_averages"]["apg"],
                "winner": player1_name if p1["career_averages"]["apg"] > p2["career_averages"]["apg"] else player2_name
            },
            "fgp": {
                "player1": p1["career_averages"]["fgp"],
                "player2": p2["career_averages"]["fgp"],
                "winner": player1_name if p1["career_averages"]["fgp"] > p2["career_averages"]["fgp"] else player2_name
            },
            "3pp": {
                "player1": p1["career_averages"]["3pp"],
                "player2": p2["career_averages"]["3pp"],
                "winner": player1_name if p1["career_averages"]["3pp"] > p2["career_averages"]["3pp"] else player2_name
            },
            "spg": {
                "player1": p1["career_averages"]["spg"],
                "player2": p2["career_averages"]["spg"],
                "winner": player1_name if p1["career_averages"]["spg"] > p2["career_averages"]["spg"] else player2_name
            },
            "bpg": {
                "player1": p1["career_averages"]["bpg"],
                "player2": p2["career_averages"]["bpg"],
                "winner": player1_name if p1["career_averages"]["bpg"] > p2["career_averages"]["bpg"] else player2_name
            },
            "tpg": {
                "player1": p1["career_averages"]["tpg"],
                "player2": p2["career_averages"]["tpg"],
                "winner": player2_name if p1["career_averages"]["tpg"] > p2["career_averages"]["tpg"] else player1_name  # Lower is better
            },
            "plus_minus": {
                "player1": p1["career_averages"]["plus_minus"],
                "player2": p2["career_averages"]["plus_minus"],
                "winner": player1_name if p1["career_averages"]["plus_minus"] > p2["career_averages"]["plus_minus"] else player2_name
            }
        },
        "overall_winner": None
    }
    
    # Determine overall winner (simple scoring system)
    p1_score = 0
    p2_score = 0
    
    if comparison["head_to_head"]["championships"]["winner"] == player1_name:
        p1_score += 3
    elif comparison["head_to_head"]["championships"]["winner"] == player2_name:
        p2_score += 3
    
    if comparison["head_to_head"]["ppg"]["winner"] == player1_name:
        p1_score += 1
    else:
        p2_score += 1
    
    if comparison["head_to_head"]["rpg"]["winner"] == player1_name:
        p1_score += 1
    else:
        p2_score += 1
    
    if comparison["head_to_head"]["apg"]["winner"] == player1_name:
        p1_score += 1
    else:
        p2_score += 1
    
    if comparison["head_to_head"]["fgp"]["winner"] == player1_name:
        p1_score += 1
    else:
        p2_score += 1
    
    # Advanced stats scoring
    if comparison["head_to_head"]["3pp"]["winner"] == player1_name:
        p1_score += 1
    else:
        p2_score += 1
    
    if comparison["head_to_head"]["spg"]["winner"] == player1_name:
        p1_score += 1
    else:
        p2_score += 1
    
    if comparison["head_to_head"]["bpg"]["winner"] == player1_name:
        p1_score += 1
    else:
        p2_score += 1
    
    if comparison["head_to_head"]["tpg"]["winner"] == player1_name:  # Lower turnovers is better
        p1_score += 1
    else:
        p2_score += 1
    
    if comparison["head_to_head"]["plus_minus"]["winner"] == player1_name:
        p1_score += 2  # Plus/minus is weighted more heavily
    else:
        p2_score += 2
    
    comparison["overall_winner"] = player1_name if p1_score > p2_score else player2_name if p2_score > p1_score else "Tie"
    comparison["scores"] = {player1_name: p1_score, player2_name: p2_score}
    
    return comparison


def print_championship_history():
    """Print all championship teams and Finals MVPs"""
    print("\n" + "="*80)
    print("NBA CHAMPIONSHIP HISTORY (1969-2024)")
    print("="*80)
    print(f"\n{'Year':<6} {'Champion Team':<30} {'Finals MVP':<25} {'PPG':<6} {'RPG':<6} {'APG':<6}")
    print("-"*80)
    
    for year in sorted(FINALS_MVP_DATABASE.keys()):
        data = FINALS_MVP_DATABASE[year]
        stats = data["stats"]
        print(f"{year:<6} {data['team']:<30} {data['mvp']:<25} {stats['ppg']:<6.1f} {stats['rpg']:<6.1f} {stats['apg']:<6.1f}")


def print_player_analysis(analysis: Dict):
    """Print detailed player analysis"""
    print("\n" + "="*80)
    print(f"CHAMPIONSHIP PLAYER ANALYSIS: {analysis['name'].upper()}")
    print("="*80)
    
    print(f"\nTotal Championships: {analysis['championships']}")
    print(f"Career Finals Averages (Championship Years):")
    print(f"  Points per Game: {analysis['career_averages']['ppg']:.1f}")
    print(f"  Rebounds per Game: {analysis['career_averages']['rpg']:.1f}")
    print(f"  Assists per Game: {analysis['career_averages']['apg']:.1f}")
    print(f"  Field Goal %: {analysis['career_averages']['fgp']:.3f}")
    print(f"\nAdvanced Analytics:")
    print(f"  3-Point %: {analysis['career_averages']['3pp']:.3f}")
    print(f"  Steals per Game: {analysis['career_averages']['spg']:.1f}")
    print(f"  Blocks per Game: {analysis['career_averages']['bpg']:.1f}")
    print(f"  Turnovers per Game: {analysis['career_averages']['tpg']:.1f}")
    print(f"  Plus/Minus: {analysis['career_averages']['plus_minus']:.1f}")
    
    print(f"\nBest Finals Performance: {analysis['best_year']}")
    if analysis['best_stats']:
        print(f"  PPG: {analysis['best_stats']['ppg']:.1f}")
        print(f"  RPG: {analysis['best_stats']['rpg']:.1f}")
        print(f"  APG: {analysis['best_stats']['apg']:.1f}")
        print(f"  FG%: {analysis['best_stats']['fgp']:.3f}")
    
    print(f"\nYear-by-Year Breakdown:")
    print(f"{'Year':<6} {'Team':<30} {'Era':<10} {'PPG':<6} {'RPG':<6} {'APG':<6} {'FG%':<6}")
    print("-"*80)
    
    for year_data in analysis['yearly_stats']:
        stats = year_data['stats']
        print(f"{year_data['year']:<6} {year_data['team']:<30} {year_data['era']:<10} "
              f"{stats['ppg']:<6.1f} {stats['rpg']:<6.1f} {stats['apg']:<6.1f} {stats['fgp']:<6.3f}")


def print_comparison(comparison: Dict):
    """Print player comparison"""
    # Check for errors first
    if "error" in comparison:
        print("\n" + "="*80)
        print("ERROR")
        print("="*80)
        print(f"\n{comparison['error']}")
        print("\nPlease make sure both players were on championship rosters.")
        print("You can use option 4 to see championship teams and rosters.")
        print("="*80)
        return
    
    p1_name = comparison["player1"]["name"]
    p2_name = comparison["player2"]["name"]
    
    print("\n" + "="*80)
    print(f"PLAYER COMPARISON: {p1_name.upper()} vs {p2_name.upper()}")
    print("="*80)
    
    print(f"\n{'Category':<20} {p1_name:<30} {p2_name:<30} {'Winner':<20}")
    print("-"*100)
    
    h2h = comparison["head_to_head"]
    
    print(f"{'Championships':<20} {h2h['championships']['player1']:<30} {h2h['championships']['player2']:<30} {h2h['championships']['winner']:<20}")
    print(f"{'PPG (Career Avg)':<20} {h2h['ppg']['player1']:<30.1f} {h2h['ppg']['player2']:<30.1f} {h2h['ppg']['winner']:<20}")
    print(f"{'RPG (Career Avg)':<20} {h2h['rpg']['player1']:<30.1f} {h2h['rpg']['player2']:<30.1f} {h2h['rpg']['winner']:<20}")
    print(f"{'APG (Career Avg)':<20} {h2h['apg']['player1']:<30.1f} {h2h['apg']['player2']:<30.1f} {h2h['apg']['winner']:<20}")
    print(f"{'FG% (Career Avg)':<20} {h2h['fgp']['player1']:<30.3f} {h2h['fgp']['player2']:<30.3f} {h2h['fgp']['winner']:<20}")
    
    print("\n" + "-"*100)
    print("ADVANCED ANALYTICS:")
    print("-"*100)
    print(f"{'3P% (Career Avg)':<20} {h2h['3pp']['player1']:<30.3f} {h2h['3pp']['player2']:<30.3f} {h2h['3pp']['winner']:<20}")
    print(f"{'SPG (Steals/G)':<20} {h2h['spg']['player1']:<30.1f} {h2h['spg']['player2']:<30.1f} {h2h['spg']['winner']:<20}")
    print(f"{'BPG (Blocks/G)':<20} {h2h['bpg']['player1']:<30.1f} {h2h['bpg']['player2']:<30.1f} {h2h['bpg']['winner']:<20}")
    print(f"{'TPG (Turnovers/G)':<20} {h2h['tpg']['player1']:<30.1f} {h2h['tpg']['player2']:<30.1f} {h2h['tpg']['winner']:<20}")
    print(f"{'Plus/Minus (Avg)':<20} {h2h['plus_minus']['player1']:<30.1f} {h2h['plus_minus']['player2']:<30.1f} {h2h['plus_minus']['winner']:<20}")
    
    print("\n" + "="*80)
    print(f"OVERALL WINNER: {comparison['overall_winner'].upper()}")
    print(f"Score: {p1_name} {comparison['scores'][p1_name]} - {comparison['scores'][p2_name]} {p2_name}")
    print("="*80)


def main():
    """Main interactive function"""
    print("="*80)
    print("NBA CHAMPIONSHIP PLAYER ANALYZER")
    print("="*80)
    print("\nThis tool analyzes NBA championship teams and player performances")
    print("from 1969 to 2024. Compare ANY players from championship rosters!")
    
    while True:
        print("\n" + "-"*80)
        print("OPTIONS:")
        print("1. View championship history (all years)")
        print("2. Analyze a specific championship player")
        print("3. Compare any two championship players")
        print("4. List all Finals MVP winners")
        print("5. View championship roster for a specific year")
        print("6. Exit")
        print("-"*80)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            print_championship_history()
        
        elif choice == "2":
            player_name = input("\nEnter championship player name: ").strip()
            analysis = analyze_player(player_name)
            
            if analysis:
                print_player_analysis(analysis)
            else:
                print(f"\nERROR: Player '{player_name}' was not on any championship roster.")
                print("Make sure you're using the exact name (e.g., 'Michael Jordan', 'Scottie Pippen', 'LeBron James')")
                print("You can use option 5 to view championship rosters for specific years.")
        
        elif choice == "3":
            player1 = input("\nEnter first player name: ").strip()
            player2 = input("Enter second player name: ").strip()
            
            comparison = compare_players(player1, player2)
            print_comparison(comparison)
        
        elif choice == "4":
            players = get_all_players()
            print("\nAll Finals MVP Winners:")
            print("-"*40)
            for i, player in enumerate(players, 1):
                years = get_player_years(player)
                print(f"{i:2}. {player:<30} ({len(years)} championship{'s' if len(years) > 1 else ''})")
        
        elif choice == "5":
            try:
                year = int(input("\nEnter year (1969-2024): ").strip())
                if year in CHAMPIONSHIP_ROSTERS:
                    data = FINALS_MVP_DATABASE[year]
                    print(f"\n{'='*80}")
                    print(f"{year} NBA CHAMPIONS: {data['team'].upper()}")
                    print(f"{'='*80}")
                    print(f"Finals MVP: {data['mvp']}")
                    print(f"\nChampionship Roster:")
                    print("-"*80)
                    roster = CHAMPIONSHIP_ROSTERS[year]
                    for i, player in enumerate(roster, 1):
                        mvp_indicator = " (Finals MVP)" if player == data['mvp'] else ""
                        print(f"{i:2}. {player}{mvp_indicator}")
                else:
                    print(f"\nYear {year} not in database. Please enter a year between 1969-2024.")
            except ValueError:
                print("\nInvalid input. Please enter a valid year (e.g., 1991, 2016).")
        
        elif choice == "6":
            print("\nThank you for using NBA Championship Player Analyzer!")
            break
        
        else:
            print("\nInvalid choice. Please enter 1-6.")


if __name__ == "__main__":

    main()
