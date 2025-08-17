from faker.providers import BaseProvider


class TeamProvider(BaseProvider):
    # Adjectives that describe the team
    adjectives = [
        'Blazing', 'Marvelous', 'Rapid', 'Valiant', 'Honorable',
        'Steadfast', 'Colossal', 'Dynamic', 'Impenetrable',
        'Menacing', 'Feral', 'Courageous', 'Transcendent', 'Epic',
        'Savage', 'Fearless', 'Agile', 'Heroic', 'Dauntless',
        'Wild', 'Audacious', 'Premier', 'Outstanding', 'Energetic',
        'Barbaric', 'Lethal', 'Majestic', 'Stellar', 'Supreme',
        'Prominent', 'Radiant', 'Treacherous', 'Mighty', 'Primal',
        'Ultimate', 'Cunning', 'Cosmic', 'Immovable', 'Blistering',
        'Intrepid', 'Daring', 'Tenacious', 'Vicious', 'Preeminent',
        'Unyielding', 'Untamed', 'Unbeatable', 'Eminent',
        'Vibrant', 'Fearsome', 'Ferocious', 'Unbreakable',
        'Rampant', 'Unshakeable', 'Noble', 'Legendary',
        'Invincible', 'Swift', 'Furious', 'Dazzling',
        'Exceptional', 'Headstrong', 'Explosive', 'Apex',
        'Gargantuan', 'Uncaged', 'Phenomenal', 'Unrelenting',
        'Resolute', 'Spirited', 'Roaring', 'Gigantic',
        'Miraculous', 'Paramount', 'Gallant', 'Titanic',
        'Vigorous', 'Stoic', 'Fierce', 'Herculean', 'Bold',
        'Spectacular', 'Unconquerable', 'Stalwart',
        'Extraordinary', 'Rampaging', 'Triumphant', 'Foremost',
        'Unstoppable', 'Ruthless', 'Intense', 'Relentless',
        'Merciless', 'Indomitable', 'Brave', 'Thunderous',
        'Formidable', 'Flawless',
    ]

    # Common entities for team names (animals, objects, mythical creatures)
    entities = [
        'Suns', 'Kraken', 'Lions', 'Yellowjackets', 'Seahawks',
        'Scorpions', 'Spiders', 'Predators', 'Rockets', 'Miners',
        'Rebels', 'Colts', 'Marauders', 'Falcons', 'Admirals',
        'Galaxy', 'Mavericks', 'Bulldogs', 'Ospreys', 'Thunder',
        'Pythons', 'Warriors', 'Blackhawks', 'Dolphins', 'Dragons',
        'Stars', 'Hornets', 'Otters', 'Comets', 'Buccaneers',
        'Panthers', 'Jets', 'Cyclones', 'Mambas', 'Rhinos',
        'Giants', 'Minotaurs', 'Hurricanes', 'Tornadoes', 'Foxes',
        'Ravens', 'Crusaders', 'Anacondas', 'Chiefs', 'Firebirds',
        'Sentinels', 'Cosmos', 'Bulls', 'Broncos', 'Mustangs',
        'Senators', 'Bills', 'Pirates', 'Gators', 'Steelers',
        'Cobras', 'Hawks', 'Renegades', 'Wolverines', 'Leopards',
        'Nomads', 'Wolves', 'Avalanche', 'Spartans', 'Explorers',
        'Commanders', 'Knights', 'Royals', 'Stingrays', 'Griffins',
        'Cheetahs', 'Leviathans', 'Navigators', 'Trailblazers',
        'Rams', 'Satellites', 'Grizzlies', 'Guardians',
        'Lightning', 'Gladiators', 'Bears', 'Raptors', 'Eagles',
        'Blizzards', 'Cougars', 'Bisons', 'Meteors', 'Unicorns',
        'Chargers', 'Pelicans', 'Raiders', 'Patriohts', 'Titans',
        'Storm', 'Phoenix', 'Tigers', 'Pioneers', 'Vikings',
        'Sharks', 'Jaguars',
    ]

    # Cities or regions to localize the team
    cities = [
        'Baghdad', 'Phnom Penh', 'Tokyo', 'Tashkent', 'Bandung',
        'Ashgabat', 'Delhi', 'Mexico City', 'Seville', 'Atlanta',
        'Lima', 'Palembang', 'Durban', 'Faisalabad', 'Cebu City',
        'Islamabad', 'Dar es Salaam', 'Los Angeles', 'Cape Town',
        'Quezon City', 'Milan', 'Lilongwe', 'New Taipei',
        'Nairobi', 'Kuwait City', 'Cologne', 'Mumbai', 'Bogotá',
        'Warsaw', 'Kanpur', 'Luanda', 'Rio de Janeiro',
        'Edinburgh', 'Lisbon', 'Melbourne', 'Alexandria',
        'New York', 'Belo Horizonte', 'Rome', 'Dubai', 'Maputo',
        'Chongqing', 'Tunis', 'Kolkata', 'Hyderabad', 'Glasgow',
        'Vancouver', 'Tainan', 'Sheffield', 'Naples', 'Tehran',
        'Freetown', 'Dhaka', 'Chicago', 'Leeds', 'Lusaka',
        'Guadalajara', 'Nagoya', 'Dublin', 'Taipei', 'Riyadh',
        'Kyiv', 'Suzhou', 'Manila', 'Nanjing', 'Bhopal', 'Calgary',
        'Davao City', 'Surabaya', 'Cardiff', 'Ahmedabad',
        'Beijing', 'Frankfurt', 'Bristol', 'Cairo', 'Windhoek',
        'Sharjah', 'Lagos', 'Patna', 'Beijing', 'Nice', 'Santiago',
        'Accra', 'Lviv', 'Mandalay', 'Tallinn', 'Harare',
        'Montevideo', 'Jeddah', 'Hamburg', 'Paris', 'Doha',
        'Colombo', 'Dongguan', 'Tripoli', 'Tianjin', 'Kigali',
        'Stuttgart', 'Istanbul', 'Nagpur', 'Gaborone', 'Miami',
        'Harbin', 'Seoul', 'Odesa', 'Budapest', 'Toulouse',
        'Almaty', 'Valencia', 'Vienna', 'Muscat', 'Berlin',
        'Barcelona', 'Bratislava', 'London', 'Karachi', 'Osaka',
        'Hong Kong', 'Busan', 'Athens', 'Addis Ababa', 'Bishkek',
        'Indore', 'Bangkok', 'Shenzhen', 'Foshan', 'Algiers',
        'Madrid', 'Birmingham', 'Kumasi', 'Kabul', 'Philadelphia',
        'Venice', 'Casablanca', 'Toronto', 'Pune', 'Bangalore',
        'Lyon', 'Monrovia', 'Ottawa', 'Vilnius', 'Shenyang',
        'Porto', 'Kampala', 'Chennai', 'Kinshasa', 'Fukuoka',
        'Boston', 'Visakhapatnam', 'Belfast', 'Medan', 'Florence',
        'Pimpri-Chinchwad', 'Sydney', 'Lucknow', 'Singapore',
        'Guangzhou', 'Jinan', 'Johannesburg', 'Khartoum',
        'Ho Chi Minh City', 'Washington', 'Yangon', 'Chengdu',
        'Marrakesh', 'Zagreb', 'Rawalpindi', 'Ivano-Frankivsk',
        'Munich', 'Wuhan', 'Kaohsiung', 'Dallas', 'Bekasi',
        'Marseille', 'Salvador', 'Jakarta', 'Kathmandu',
        'Montreal', 'Surat', 'Phoenix', 'Prague', 'Manchester',
        'Vientiane', 'Dushanbe', 'Dakar', 'Seattle', 'Lahore',
        'Qingdao', 'Dalian', 'Kuala Lumpur', 'Shanghai',
        'Ulaanbaatar', 'Buenos Aires', 'Liverpool', 'Thane',
        'Abu Dhabi', 'Hangzhou', 'Manama', 'Houston', 'Malaga',
    ]

    patterns = (
        '{entity}',
        '{city} {entity}',
        '{adjective} {entity}',
        '{city} {adjective} {entity}',
    )

    def team_name(self):
        """Generate a realistic team name using simple patterns."""
        pattern = self.random_element(self.patterns)
        return pattern.format(
            entity=self.random_element(self.entities),
            adjective=self.random_element(self.adjectives),
            city=self.random_element(self.cities),
        )
