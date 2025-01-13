"""
########################################################################
The tables.py module includes the FAO56Tables class, which contains
suggested values for attributes of the Parameters class as defined in
FAO-56, specifically in Tables 11, 12, 17, and 22.

FAO-56 Table 11 - Lengths of crop development stages
FAO-56 Table 12 - Single crop coefficients (Kc)
FAO-56 Table 17 - Basal crop coefficients (Kcb)
FAO-56 Table 22 - Maximum root depth (Zr) and depletion fraction (p)

The tables.py module contains the following:
    FAO56Tables - A class for specifying parameter values as defined in
                  FAO-56 tables.

12/12/2024 FAOTables class created by Reagan Ames and Tyler Pokoski
01/08/2024 Modification for release
########################################################################
"""

class FAO56Tables:
    '''
    The following assumptions were made to determine the most applicable
    values from the FAO56 tables.
      For tables 12, 17, and 22 -
            Assume left most value in range
            Assume unstressed conditions
                  For fruit trees assume active ground cover and no frosts
                  For Citrus assume 70% canopy cover
                  For tropical trees assume ground cover
                  For Tea assume unshaded conditions
            For forages assume “individual cutting period” for basic value
            Assume sweet maize is harvested fresh for human consumption
            Assume field maize is allowed to dry before harvest
            Beans, legumes, tomatoes, peppers, and cucumbers do not reach a
            height greater than 1.5 to 2m in height
            For oil crops, assume higher value coorelated with rainfed crops
            Wheat is not hand harvested
        For table 11 -
            Prioritize values based on climate in the following order:
                    Continental Climates
                    Central USA
                    35-45 degree latitude
                    Texas
                    Idaho
                    Arizona
                    California
                    California, Desert
                    Hawaii
                    Semi Arid
                    Arid
                    Europe
                    Mediterranean
                    Mediterranean & Arid
                    Italy
                    Warm Winter
                    West Africa
                    Near East (desert)
                    Tropical Regions
                    High Latitudes
            Second default by planting date (after defaulting climates)
                  Spring before fall
            Assume crucifer values for Brussel sprouts
            For any ranges, assume leftmost value
            Assume 1st year of growth for artichokes
            Sweet Maize is harvested fresh
            Assume alfalfa and sudan have already been harvested once 
            (other cutting cycles)
            Sugar cane is ratoon
            For any of the following crops not included in table 11, default
            growth stage values to Field Maize:
                      Garlic
                      Parsnip
                      Turnip (and Rutabaga)
                      Chickpea
                      Garbanzo
                      Mint
                      Strawberries
                      Rapeseed, Canola
                      Clover hay, Berseem
                      Rye Grass Hay
                      Grazing Pasture
                      Turf Grass
                      Cacao
                      Coffee
                      Date Palms
                      Palm Trees
                      Rubber Trees
                      Tea
                      Berries (bushes)
                      Almonds
                      Avocado
                      Conifer Trees
                      Kiwi
    '''

    def __init__(self):
      """Initialize the FAO56Tables class attributes."""

      #FAO-56 Table 11. Lengths of crop development stages for various
      #planting periods and climatic regions (days)
      tabel11 = """
      Crop,                        Lini, Ldev, Lmid, Llate,Total,Plant Date, Region
      Broccoli,                      35,   45,   40,    15,  135,      Sept, Calif. Desert USA
      Cabbage,                       40,   60,   50,    15,  165,      Sept, Calif. Desert USA
      Carrots,                       20,   30,   30,    20,  100,   Oct/Jan, Arid climate
      Carrots,                       30,   40,   60     20,  150,   Feb/Mar, Mediterranean
      Carrots,                       30,   50,   90,    30,  200,       Oct, Calif. Desert USA
      Cauliflower,                   35,   50,   40,    15,  140,      Sept, Calif. Desert USA
      Celery,                        30,   55,  105,    20,  210, 
      Lettuce,                       25,   35,   30,    10,  100, 
      Onions (dry),                  20,   35,  110,    45,  210, 
      Onions (green),                30,   55,   55,    40,  180,
      Onions(seed),                  20,   45,  165,    45,  275,
      Spinach,                       20,   30,   40,    10,  100,
      Radish,                        10,   10,   15,     5,   40,
      EggPlant                ,                      30,   40,   40,    20,  130,
      SweetPeppers(bell)      ,            30,   40,  110,    30,  210,
      Tomato                  ,                        35,   40,   50,    30,  155,
      Cantaloupe              ,                    30,   45,   35,    10,  120,
      Cucumber(FreshMarket)   ,         20,   30,   40,    15,  105,
      Cucumber(MachineHarvest),      20,   30,   40,    15,  105,
      Pumpkin,Winter,Squash,          25,   35,   35,    25,  120,
      Squash,Zucchini,               25,   35,   25,    15,  100,
      SweetMelons,                   30,   30,   50,    30,  140,
      Watermelon,                    20,   30,   30,    30,  110,
      Beets,table,                   25,   30,   25,    10,   90,
      Cassava(year1),                20,   40,   90,    60,  210,
      Cassava(year2),               150,   40,  110,    60,  360,
      Potato,                        45,   30,   70,    20,  165,
      SweetPotato,                   20,   30,   60,    40,  150,
      SugarBeet,                     50,   40,   50,    40,  180,
      Beans,green,                   15,   25,   25,    10,   75,
      Beans,dryandPulses,            20,   30,   40,    20,  110,
      Fababean(Fresh),               15,   25,   35,    15,   90,
      Fababean(Dry),                 15,   25,   35,    15,   90,
      GreenGramandCowpeas(Fresh),    20,   30,   30,    20,  110,
      GreenGramandCowpeas(Dry),      20,   30,   30,    20,  110,
      Groundnut(Peanut),             35,   45,   35,    25,  140,
      Lentil,                        25,   35,   70,    40,  170,
      Peas(Fresh),                   35,   25,   30,    20,  110,
      Peas(Dry),                     35,   25,   30,    20,  110,
      Soybeans,                      20,   30,   60,    25,  140,
      Artichokes,                    40,   40,  250,    30,  360,
      Asparagus,                     90,   30,  200,    45,  365,
      Cotton,                        30,   50,   55,    45,  180,
      Flax,                          30,   40,  100,    50,  220,
      Castorbean(Ricinus),           25,   40,   65,    50,  180,
      Safflower,                     20,   35,   45,    25,  125,
      Sesame,                        20,   30,   40,    20,  100,
      Sunflower,                     25,   35,   45,    25,  130,
      Barley,                        20,   25,   60,    30,  135,
      Oats,                          20,   25,   60,    30,  135,
      SpringWheat,                   20,   25,   60,    30,  135,
      WinterWheat(FrozenSoils),     160,   75,   75,    25,  335,
      WinterWheat(Non-FrozenSoils), 160,   75,   75,    25,  335,
      Maize,Field(grain),            30,   40,   50,    50,  170,
      Maize,Sweet(sweetcorn),        30,   30,   30,    10,  110,
      Millet ,                       20,   30,   55,    35,  140,
      Sorghum(Grain),                20,   25,   40,    30,  130,
      Sorghum(Sweet),                20,   25,   40,    30,  130,
      Rice,                          30,   30,   60,    30,  150,
      AlfalfaHay,                     5,   20,   10,    10,   45,
      AlfalfaHay(seed),               5,   20,   10,    10,   45,
      Bermudahay,                    10,   15,   75,    35,  135,
      Bermudahay(seed),              10,   25,   35,    35,  105,
      SudanGrasshay(annual),          3,   15,   12,     7,   37,
      SugarCane,                     35,  105,  210,    70,  420,
      Banana(1styear),              120,   90,  120,    60,  390,
      Banana(2ndyear),              120,   60,  180,     5,  365,
      Pineapple,                     60,  120,  600,    10,  790,
      Grapes(TableorRaisin),         20,   50,   75,    60,  205,
      Grapes(Wine),                  20,   50,   75,    60,  205,
      Hops,                          25,   40,   80,    10,  155,
      Apples,Cherries,Pears,         30,   50,  130,    30,  240,
      Apricots,Peaches,StoneFruit,   30,   50,  130,    30,  240,
      Citrus,                        60,   90,  120,    95,  365,
      Olives,                        30,   90,   60,    90,  270,
      Pistachios,                    20,   60,   30,    40,  150,
      WalnutOrchard,                 20,   10,  130,    30,  190,

      
      
      
      
      self.tables = {
        'Broccoli': {'Kcini': 0.7, 'Kcmid': 1.05, 'Kcend': 0.95, 'h': 0.3,
                     'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.85, 
                     'Zrmax': 0.4, 'p': 0.45},
        'Brussel Sprouts': {'Kcini': 0.7, 'Kcmid': 1.05, 'Kcend': 0.95, 
                            'h': 0.4, 'Kcbini': 0.15, 'Kcbmid': 0.95, 
                            'Kcbend': 0.85, 'Zrmax': 0.4, 'p': 0.45}, 
        'Cabbage': {'Kcini': 0.7, 'Kcmid': 1.05, 'Kcend': 0.95, 'h': 0.4,
                    'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.85, 
                    'Zrmax': 0.5, 'p': 0.45}, 
        'Carrots': {'Kcini': 0.7, 'Kcmid': 1.05, 'Kcend': 0.95, 'h': 0.3,
                    'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.85, 
                    'Zrmax': 0.5, 'p': 0.35}, 
        'Cauliflower': {'Kcini': 0.7, 'Kcmid': 1.05, 'Kcend': 0.95,
                        'h': 0.4, 'Kcbini': 0.15, 'Kcbmid': 0.95, 
                        'Kcbend': 0.85, 'Zrmax': 0.4, 'p': 0.45}, 
        'Celery': {'Kcini': 0.7, 'Kcmid': 1.05, 'Kcend': 1.0, 'h': 0.6,
                   'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.9, 
                   'Zrmax': 0.3, 'p': 0.2}, 
        'Garlic': {'Kcini': 0.7, 'Kcmid': 1, 'Kcend': 0.7, 'h': 0.3, 
                   'Kcbini': 0.15, 'Kcbmid': 0.9, 'Kcbend': 0.6, 
                   'Zrmax': 0.3, 'p': 0.3}, 
        'Lettuce': {'Kcini': 0.7, 'Kcmid': 1, 'Kcend': 0.95, 'h': 0.3,
                    'Kcbini': 0.15, 'Kcbmid': 0.9, 'Kcbend': 0.9, 
                    'Zrmax': 0.3, 'p': 0.3}, 
        'Onions (dry)': {'Kcini': 0.7, 'Kcmid': 1.05, 'Kcend': 0.75,
                         'h': 0.4, 'Kcbini': 0.15, 'Kcbmid': 0.95, 
                         'Kcbend': 0.65, 'Zrmax': 0.3, 'p': 0.3},
        'Onions (green)': {'Kcini': 0.7, 'Kcmid': 1, 'Kcend': 1.0, 
                           'h': 0.3, 'Kcbini': 0.15, 'Kcbmid': 0.9, 
                           'Kcbend': 0.9, 'Zrmax': 0.3, 'p': 0.3}, 
        'Onions (seed)': {'Kcini': 0.7, 'Kcmid': 1.05, 'Kcend': 0.8,
                          'h': 0.5, 'Kcbini': 0.15, 'Kcbmid': 1.05, 
                          'Kcbend': 0.7, 'Zrmax': 0.3, 'p': 0.35},
        'Spinach': {'Kcini': 0.7, 'Kcmid': 1, 'Kcend': 0.95, 'h': 0.3,
                    'Kcbini': 0.15, 'Kcbmid': 0.9, 'Kcbend': 0.85, 
                    'Zrmax': 0.3, 'p': 0.2}, 
        'Radish': {'Kcini': 0.7, 'Kcmid': 0.9, 'Kcend': 0.85, 'h': 0.3,
                   'Kcbini': 0.15, 'Kcbmid': 0.85, 'Kcbend': 0.75, 
                   'Zrmax': 0.3, 'p': 0.3}, 
        'Egg Plant': {'Kcini': 0.6, 'Kcmid': 1.05, 'Kcend': 0.9, 
                      'h': 0.8, 'Kcbini': 0.15, 'Kcbmid': 1.0, 
                      'Kcbend': 0.8, 'Zrmax': 0.7, 'p': 0.45}, 
        'Sweet Peppers (bell)': {'Kcini': 0.6, 'Kcmid': 1.05,
                                 'Kcend': 0.9, 'h': 0.7, 'Kcbini': 0.15, 
                                 'Kcbmid': 1.0, 'Kcbend': 0.8, 
                                 'Zrmax': 0.5, 'p': 0.3}, 
        'Tomato': {'Kcini': 0.6, 'Kcmid': 1.15, 'Kcend': 0.7, 'h': 0.6,
                   'Kcbini': 0.15, 'Kcbmid': 1.1, 'Kcbend': 0.6, 
                   'Zrmax': 0.7, 'p': 0.4}, 
        'Cantaloupe': {'Kcini': 0.5, 'Kcmid': 0.85, 'Kcend': 0.6, 
                       'h': 0.3, 'Kcbini': 0.15, 'Kcbmid': 0.75, 
                       'Kcbend': 0.5, 'Zrmax': 0.9, 'p': 0.45}, 
        'Cucumber (Fresh Market)': {'Kcini': 0.6, 'Kcmid': 1, 
                                    'Kcend': 0.75, 'h': 0.3, 
                                    'Kcbini': 0.15, 'Kcbmid': 0.95, 
                                    'Kcbend': 0.7, 'Zrmax': 0.7, 
                                    'p': 0.5}, 
        'Cucumber (Machine Harvest)': {'Kcini': 0.5, 'Kcmid': 1, 
                                       'Kcend': 0.9, 'h': 0.3, 
                                       'Kcbini': 0.15, 'Kcbmid': 0.95, 
                                       'Kcbend': 0.8, 'Zrmax': 0.7, 
                                       'p': 0.5}, 
        'Pumpkin, Winter Squash': {'Kcini': 0.5, 'Kcmid': 1, 'Kcend': 0.8,
                                   'h': 0.4, 'Kcbini': 0.15, 
                                   'Kcbmid': 0.95, 'Kcbend': 0.7, 
                                   'Zrmax': 1.0, 'p': 0.35}, 
        'Squash, Zucchini': {'Kcini': 0.5, 'Kcmid': 0.95, 'Kcend': 0.75,
                             'h': 0.3, 'Kcbini': 0.15, 'Kcbmid': 0.9, 
                             'Kcbend': 0.7, 'Zrmax': 0.6, 'p': 0.5}, 
        'Sweet Melons': {'Kcini': 0.5, 'Kcmid': 1.05, 'Kcend': 0.75,
                         'h': 0.4, 'Kcbini': 0.15, 'Kcbmid': 1.0, 
                         'Kcbend': 0.7, 'Zrmax': 0.8, 'p': 0.4}, 
        'Watermelon': {'Kcini': 0.4, 'Kcmid': 1, 'Kcend': 0.75, 'h': 0.4, 
                       'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.7, 
                       'Zrmax': 0.8, 'p': 0.4}, 
        'Beets, table':{'Kcini': 0.5, 'Kcmid': 1.05, 'Kcend': 0.95,
                        'h': 0.4, 'Kcbini': 0.15, 'Kcbmid': 0.95, 
                        'Kcbend': 0.85, 'Zrmax': 0.6, 'p': 0.5}, 
        'Cassava (year 1)': {'Kcini': 0.3, 'Kcmid': 0.8, 'Kcend': 0.3,
                             'h': 1.0, 'Kcbini': 0.15, 'Kcbmid': 0.7, 
                             'Kcbend': 0.2, 'Zrmax': 0.5, 'p': 0.35}, 
        'Cassava (year 2)': {'Kcini': 0.3, 'Kcmid': 1.1, 'Kcend': 0.5,
                             'h': 1.5, 'Kcbini': 0.15, 'Kcbmid': 1.0, 
                             'Kcbend': 0.45, 'Zrmax': 0.7, 'p': 0.4}, 
        'Parsnip': {'Kcini': 0.5, 'Kcmid': 1.05, 'Kcend': 0.95, 'h': 0.4,
                    'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.85, 
                    'Zrmax': 0.5, 'p': 0.4}, 
        'Potato': {'Kcini': 0.5, 'Kcmid': 1.15, 'Kcend': 0.75, 'h': 0.6, 
                   'Kcbini': 0.15, 'Kcbmid': 1.1, 'Kcbend': 0.65, 
                   'Zrmax': 0.4, 'p': 0.35}, 
        'Sweet Potato': {'Kcini': 0.5, 'Kcmid': 1.15, 'Kcend': 0.65, 
                         'h': 0.4, 'Kcbini': 0.15, 'Kcbmid': 1.1, 
                         'Kcbend': 0.55, 'Zrmax': 1.0, 'p': 0.65}, 
        'Turnip (and Rutabaga)': {'Kcini': 0.5, 'Kcmid': 1.1,
                                  'Kcend': 0.95, 'h': 0.6,'Kcbini': 0.15, 
                                  'Kcbmid': 1.0, 'Kcbend': 0.85, 
                                  'Zrmax': 0.5, 'p': 0.5}, 
        'Sugar Beet': {'Kcini': 0.35, 'Kcmid': 1.2, 'Kcend': 0.7, 
                       'h': 0.5, 'Kcbini': 0.15, 'Kcbmid': 1.15, 
                       'Kcbend': 0.5, 'Zrmax': 0.7, 'p': 0.55}, 
        'Beans, green': {'Kcini': 0.5, 'Kcmid': 1.05, 'Kcend': 0.9, 
                         'h': 0.4, 'Kcbini': 0.15, 'Kcbmid': 1.0,
                         'Kcbend': 0.8, 'Zrmax': 0.5, 'p': 0.45}, 
        'Beans, dry and Pulses': {'Kcini': 0.4, 'Kcmid': 1.15,
                                  'Kcend': 0.35, 'h': 0.4, 'Kcbini': 0.15, 
                                  'Kcbmid': 1.1, 'Kcbend': 0.25, 
                                  'Zrmax': 0.6, 'p': 0.45}, 
        'Chick pea': {'Kcini': 0.4, 'Kcmid': 1, 'Kcend': 0.35, 'h': 0.4,
                      'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.25, 
                      'Zrmax': 0.6, 'p': 0.5}, 
        'Fababean (Fresh)': {'Kcini': 0.5, 'Kcmid': 1.15, 'Kcend': 1.1, 
                             'h': 0.8, 'Kcbini': 0.15, 'Kcbmid': 1.10, 
                             'Kcbend': 1.05, 'Zrmax': 0.5, 'p': 0.45}, 
        'Fababean (Dry)': {'Kcini': 0.5, 'Kcmid': 1.15, 'Kcend': 0.3,
                           'h': 0.8, 'Kcbini': 0.15, 'Kcbmid': 1.10, 
                           'Kcbend': 0.2, 'Zrmax': 0.5, 'p': 0.45}, 
        'Grabanzo': {'Kcini': 0.4, 'Kcmid': 1.15, 'Kcend': 0.35, 'h': 0.8,
                     'Kcbini': 0.15, 'Kcbmid': 1.05, 'Kcbend': 0.25, 
                     'Zrmax': 0.6, 'p': 0.45}, 
        'Green Gram and Cowpeas (Fresh)': {'Kcini': 0.4, 'Kcmid': 1.05,
                                           'Kcend': 0.6, 'h': 0.4, 
                                           'Kcbini': 0.15, 'Kcbmid': 1.0, 
                                           'Kcbend': 0.55, 'Zrmax': 0.6, 
                                           'p': 0.45}, 
        'Green Gram and Cowpeas (Dry)': {'Kcini': 0.4, 'Kcmid': 1.05,
                                         'Kcend': 0.35, 'h': 1.4, 
                                         'Kcbini': 0.15, 'Kcbmid': 1.0, 
                                         'Kcbend': 0.25, 'Zrmax': 0.6, 
                                         'p': 0.45}, 
        'Groundnut (Peanut)': {'Kcini': 0.4, 'Kcmid': 1.15, 'Kcend': 0.6, 
                               'h': 0.4, 'Kcbini': 0.15, 'Kcbmid': 1.1, 
                               'Kcbend': 0.5, 'Zrmax': 0.5, 'p': 0.5}, 
        'Lentil': {'Kcini': 0.4, 'Kcmid': 1.1, 'Kcend': 0.3, 'h': 0.5,
                   'Kcbini': 0.15, 'Kcbmid': 1.05, 'Kcbend': 0.2, 
                   'Zrmax': 0.6, 'p': 0.5}, 
        'Peas (Fresh)': {'Kcini': 0.5, 'Kcmid': 1.15, 'Kcend': 1.1, 
                         'h': 0.5, 'Kcbini': 0.15, 'Kcbmid': 1.1, 
                         'Kcbend': 1.05, 'Zrmax': 0.6, 'p': 0.35}, 
        'Peas (Dry)': {'Kcini': 0.5, 'Kcmid': 1.15, 'Kcend': 0.3,
                       'h': 0.5, 'Kcbini': 0.15, 'Kcbmid': 1.1, 
                       'Kcbend': 0.2, 'Zrmax': 0.6, 'p': 0.4}, 
        'Soybeans': {'Kcini': 0.4, 'Kcmid': 1.15, 'Kcend': 0.5, 'h': 0.5,
                     'Kcbini': 0.15, 'Kcbmid': 1.1, 'Kcbend': 0.3, 
                     'Zrmax': 0.6, 'p': 0.5}, 
        'Artichokes': {'Kcini': 0.5, 'Kcmid': 1, 'Kcend': 0.95, 'h': 0.7,
                       'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.9, 
                       'Zrmax': 0.6, 'p': 0.45}, 
        'Asparagus': {'Kcini': 0.5, 'Kcmid': 0.95, 'Kcend': 0.3, 'h': 0.2,
                      'Kcbini': 0.15, 'Kcbmid': 0.9, 'Kcbend': 0.2, 
                      'Zrmax': 1.2, 'p': 0.45}, 
        'Mint': {'Kcini': 0.6, 'Kcmid': 1.15, 'Kcend': 1.1, 'h': 0.6,
                 'Kcbini': 0.4, 'Kcbmid': 1.1, 'Kcbend': 1.05, 
                 'Zrmax': 0.4, 'p': 0.4}, 
        'Strawberries': {'Kcini': 0.4, 'Kcmid': 0.85, 'Kcend': 0.75, 
                         'h': 0.2, 'Kcbini': 0.3, 'Kcbmid': 0.8, 
                         'Kcbend': 0.7, 'Zrmax': 0.2, 'p': 0.2}, 
        'Cotton': {'Kcini': 0.35, 'Kcmid': 1.15, 'Kcend': 0.7, 'h': 1.2, 
                   'Kcbini': 0.15, 'Kcbmid': 1.1, 'Kcbend': 0.5, 
                   'Zrmax': 1.0, 'p': 0.65}, 
        'Flax': {'Kcini': 0.35, 'Kcmid': 1.1, 'Kcend': 0.25, 'h': 1.2,
                 'Kcbini': 0.15, 'Kcbmid': 1.05, 'Kcbend': 0.2, 
                 'Zrmax': 1.0, 'p': 0.5}, 
        'Sisal': {'Kcini': 0.35, 'Kcmid': 0.4, 'Kcend': 0.4, 'h': 1.5,
                  'Kcbini': 0.15, 'Kcbmid': 0.4, 'Kcbend': 0.4, 
                  'Zrmax': 0.5, 'p': 0.8}, 
        'Castorbean (Ricinus)': {'Kcini': 0.35, 'Kcmid': 1.15,
                                 'Kcend': 0.55, 'h': 0.3, 'Kcbini': 0.15, 
                                 'Kcbmid': 1.1, 'Kcbend': 0.45, 
                                 'Zrmax': 1.0, 'p': 0.5}, 
        'Rapeseed, Canola': {'Kcini': 0.35, 'Kcmid': 1.15, 'Kcend': 0.35, 
                             'h': 0.6, 'Kcbini': 0.15, 'Kcbmid': 1.1, 
                             'Kcbend': 0.25, 'Zrmax': 1.0, 'p': 0.6}, 
        'Safflower': {'Kcini': 0.35, 'Kcmid': 1.15, 'Kcend': 0.25,
                      'h': 0.8, 'Kcbini': 0.15, 'Kcbmid': 1.1, 
                      'Kcbend': 0.2, 'Zrmax': 1.0, 'p': 0.6}, 
        'Sesame': {'Kcini': 0.35, 'Kcmid': 1.1, 'Kcend': 0.25, 'h': 1.0,
                   'Kcbini': 0.15, 'Kcbmid': 1.05, 'Kcbend': 0.2, 
                   'Zrmax': 1.0, 'p': 0.6}, 
        'Sunflower': {'Kcini': 0.35, 'Kcmid': 1.15, 'Kcend': 0.35,
                      'h': 2.0, 'Kcbini': 0.15, 'Kcbmid': 1.1, 
                      'Kcbend': 0.25, 'Zrmax': 0.8, 'p': 0.45}, 
        'Barley': {'Kcini': 0.3, 'Kcmid': 1.15, 'Kcend': 0.25, 'h': 1.0,
                   'Kcbini': 0.15, 'Kcbmid': 1.1, 'Kcbend': 0.15, 
                   'Zrmax': 1.0, 'p': 0.55}, 
        'Oats': {'Kcini': 0.3, 'Kcmid': 1.15, 'Kcend': 0.25, 'h': 1.0,
                 'Kcbini': 0.15, 'Kcbmid': 1.1, 'Kcbend': 0.15, 
                 'Zrmax': 1.0, 'p': 0.55}, 
        'Spring Wheat': {'Kcini': 0.3, 'Kcmid': 1.15, 'Kcend': 0.25,
                         'h': 1.0, 'Kcbini': 0.15, 'Kcbmid': 1.1, 
                         'Kcbend': 0.15, 'Zrmax': 1.0, 'p': 0.55}, 
        'Winter Wheat (Frozen Soils)': {'Kcini': 0.4, 'Kcmid': 1.15,
                                        'Kcend': 0.25, 'h': 1.0, 
                                        'Kcbini': 0.15, 'Kcbmid': 1.1, 
                                        'Kcbend': 0.15, 'Zrmax': 1.5, 
                                        'p': 0.55}, 
        'Winter Wheat (Non - Frozen Soils)': {'Kcini': 0.7, 'Kcmid': 1.15,
                                              'Kcend': 0.25, 'h': 1.0, 
                                              'Kcbini': 0.15, 
                                              'Kcbmid': 1.1, 
                                              'Kcbend': 0.15, 
                                              'Zrmax': 1.5,'p': 0.55}, 
        'Maize, Field (grain)': {'Kcini': 0.3, 'Kcmid': 1.2,
                                 'Kcend': 0.6, 'h': 2.0, 'Kcbini': 0.15, 
                                 'Kcbmid': 1.15, 'Kcbend': 0.5, 
                                 'Zrmax': 1.0, 'p': 0.55}, 
        'Maize, Sweet (sweet corn)': {'Kcini': 0.3, 'Kcmid': 1.15,
                                      'Kcend': 1.05, 'h': 1.5, 
                                      'Kcbini': 0.15, 'Kcbmid': 1.1, 
                                      'Kcbend': 1.0, 'Zrmax': 0.8, 
                                      'p': 0.5}, 
        'Millet': {'Kcini': 0.3, 'Kcmid': 1, 'Kcend': 0.3, 'h': 1.5,
                   'Kcbini': 0.15, 'Kcbmid': 0.95, 'Kcbend': 0.2, 
                   'Zrmax': 1.0, 'p': 0.55}, 
        'Sorghum (Grain)': {'Kcini': 0.3, 'Kcmid': 1, 'Kcend': 0.55,
                            'h': 1.0, 'Kcbini': 0.15, 'Kcbmid': 0.95, 
                            'Kcbend': 0.35, 'Zrmax': 1.0, 'p': 0.55}, 
        'Sorghum (Sweet)': {'Kcini': 0.3, 'Kcmid': 1.2, 'Kcend': 1.05, 
                            'h': 2.0, 'Kcbini': 0.15, 'Kcbmid': 1.15, 
                            'Kcbend': 1.0, 'Zrmax': 1.0, 'p': 0.5}, 
        'Rice': {'Kcini': 1.05, 'Kcmid': 1.2, 'Kcend': 0.9, 'h': 1.0,
                 'Kcbini': 1.0, 'Kcbmid': 1.15, 'Kcbend': 0.7, 
                 'Zrmax': 0.5, 'p': 0.2}, 
        'Alfalfa Hay': {'Kcini': 0.4, 'Kcmid': 0.95, 'Kcend': 0.9,
                        'h': 0.7, 'Kcbini': 0.3, 'Kcbmid': 1.15, 
                        'Kcbend': 1.1, 'Zrmax': 1.0, 'p': 0.55}, 
        'Alfalfa Hay (seed)': {'Kcini': 0.4, 'Kcmid': 0.5, 'Kcend': 0.5, 
                               'h': 0.7, 'Kcbini': 0.3, 'Kcbmid': 0.45, 
                               'Kcbend': 0.45, 'Zrmax': 1.0, 'p': 0.6}, 
        'Bermuda hay': {'Kcini': 0.55, 'Kcmid': 1.00, 'Kcend': 0.85, 
                        'h': 0.35, 'Kcbini': 0.5, 'Kcbmid': 0.95, 
                        'Kcbend': 0.8, 'Zrmax': 1.0, 'p': 0.55}, 
        'Bermuda hay (seed)': {'Kcini': 0.35, 'Kcmid': 0.9,
                               'Kcend': 0.65, 'h': 0.4, 'Kcbini': 0.15, 
                               'Kcbmid': 0.85, 'Kcbend': 0.6, 
                               'Zrmax': 1.0, 'p': 0.6}, 
        'Clover hay, Berseem': {'Kcini': 0.4, 'Kcmid': 0.90,
                                'Kcend': 0.85, 'h': 0.6, 'Kcbini': 0.3, 
                                'Kcbmid': 1.1, 'Kcbend': 1.05, 
                                'Zrmax': 0.6, 'p': 0.5}, 
        'Rye Grass hay': {'Kcini': 0.95, 'Kcmid': 1.05, 'Kcend': 1.0,
                          'h': 0.3, 'Kcbini': 0.85, 'Kcbmid': 1.0, 
                          'Kcbend': 0.95, 'Zrmax': 0.6,'p': 0.6}, 
        'Sudan Grass hay (annual)': {'Kcini': 0.5, 'Kcmid': 0.90, 
                                      'Kcend': 0.85, 'h': 1.2, 
                                      'Kcbini': 0.3, 'Kcbmid': 1.1, 
                                      'Kcbend': 1.05, 'Zrmax': 1.0, 
                                      'p': 0.55}, 
        'Grazing Pasture (Rotated)': {'Kcini': 0.4, 'Kcmid': 0.85, 
                                      'Kcend': 0.85, 'h': 0.15, 
                                      'Kcbini': 0.3, 'Kcbmid': 0.8, 
                                      'Kcbend': 0.8, 'Zrmax': 0.5, 
                                      'p': 0.6}, 
        'Grazing Pasture': {'Kcini': 0.3, 'Kcmid': 0.75, 'Kcend': 0.75, 
                            'h': 0.1, 'Kcbini': 0.3, 'Kcbmid': 0.7, 
                            'Kcbend': 0.7,'Zrmax': 0.5, 'p': 0.6}, 
        'Turf grass (cool season)': {'Kcini': 0.9, 'Kcmid': 0.95, 
                                      'Kcend': 0.95, 'h': 0.1, 
                                      'Kcbini': 0.85, 'Kcbmid': 0.9, 
                                      'Kcbend': 0.9, 'Zrmax': 0.5, 
                                      'p': 0.4}, 
        'Turf grass (warm season)': {'Kcini': 0.8, 'Kcmid': 0.85, 
                                      'Kcend': 0.85, 'h': 0.1, 
                                      'Kcbini': 0.75, 'Kcbmid': 0.8, 
                                      'Kcbend': 0.8, 'Zrmax': 0.5, 
                                      'p': 0.5}, 
        'Sugar Cane': {'Kcini': 0.4, 'Kcmid': 1.25, 'Kcend': 0.75, 
                        'h': 3.0, 'Kcbini': 0.15, 'Kcbmid': 1.2, 
                        'Kcbend': 0.7, 'Zrmax': 1.2, 'p': 0.65}, 
        'Banana (1st year)': {'Kcini': 0.5, 'Kcmid': 1.1, 'Kcend': 1.0, 
                              'h': 3.0, 'Kcbini': 0.15, 'Kcbmid': 1.05, 
                              'Kcbend': 0.9, 'Zrmax': 0.5, 'p': 0.35}, 
        'Banana (2nd year)': {'Kcini': 1.0, 'Kcmid': 1.2, 'Kcend': 1.1, 
                              'h': 4.0, 'Kcbini': 0.6, 'Kcbmid': 1.1, 
                              'Kcbend': 1.05, 'Zrmax': 0.5, 'p': 0.35}, 
        'Cacao': {'Kcini': 1.0, 'Kcmid': 1.05, 'Kcend': 1.05, 'h': 3.0, 
                  'Kcbini': 0.9, 'Kcbmid': 1.0, 'Kcbend': 1.0, 
                  'Zrmax': 0.7, 'p': 0.3}, 
        'Coffee': {'Kcini': 1.05, 'Kcmid': 1.1, 'Kcend': 1.1, 'h': 2.0, 
                    'Kcbini': 1.0, 'Kcbmid': 1.05, 'Kcbend': 1.05, 
                    'Zrmax': 0.9, 'p': 0.4}, 
        'Date Palms': {'Kcini': 0.9, 'Kcmid': 0.95, 'Kcend': 0.95, 
                        'h': 8.0, 'Kcbini': 0.8, 'Kcbmid': 0.85, 
                        'Kcbend': 0.85, 'Zrmax': 1.5, 'p': 0.5}, 
        'Palm Trees': {'Kcini': 0.95, 'Kcmid': 1, 'Kcend': 1.0, 'h': 8.0, 
                        'Kcbini': 0.85, 'Kcbmid': 0.9, 'Kcbend': 0.9, 
                        'Zrmax': 0.7, 'p': 0.65}, 
        'Pineapple': {'Kcini': 0.5, 'Kcmid': 0.5, 'Kcend': 0.5, 'h': 0.6, 
                      'Kcbini': 0.3, 'Kcbmid': 0.45, 'Kcbend': 0.45, 
                      'Zrmax': 0.3,'p': 0.5}, 
        'Rubber Trees': {'Kcini': 0.95, 'Kcmid': 1, 'Kcend': 1.0, 
                          'h': 10.0, 'Kcbini': 0.85, 'Kcbmid': 0.9, 
                          'Kcbend': 0.9, 'Zrmax': 1.0, 'p': 0.4}, 
        'Tea': {'Kcini': 0.95, 'Kcmid': 1, 'Kcend': 1.0, 'h': 1.5, 
                'Kcbini': 0.9,'Kcbmid': 0.95, 'Kcbend': 0.9, 
                'Zrmax': 0.9, 'p': 0.4}, 
        'Berries (bushes)': {'Kcini': 0.3, 'Kcmid': 1.05, 'Kcend': 0.5, 
                              'h': 1.5, 'Kcbini': 0.2, 'Kcbmid': 1.0, 
                              'Kcbend': 0.4, 'Zrmax': 0.6, 'p': 0.5}, 
        'Grapes (Table or Raisin)': {'Kcini': 0.3, 'Kcmid': 0.85, 
                                      'Kcend': 0.45, 'h': 2.0, 
                                      'Kcbini': 0.15, 'Kcbmid': 0.8, 
                                      'Kcbend': 0.4, 'Zrmax': 1.0, 
                                      'p': 0.35}, 
        'Grapes (Wine)': {'Kcini': 0.3, 'Kcmid': 0.7, 'Kcend': 0.45, 
                          'h': 1.5, 'Kcbini': 0.15, 'Kcbmid': 0.65, 
                          'Kcbend': 0.4, 'Zrmax': 1.0, 'p': 0.45}, 
        'Hops': {'Kcini': 0.3, 'Kcmid': 1.05, 'Kcend': 0.85, 'h': 5.0, 
                  'Kcbini': 0.15, 'Kcbmid': 1.0, 'Kcbend': 0.8, 
                  'Zrmax': 1.0, 'p': 0.5}, 
        'Almonds': {'Kcini': 0.4, 'Kcmid': 0.9, 'Kcend': 0.65, 'h': 5.0, 
                    'Kcbini': 0.2, 'Kcbmid': 0.85, 'Kcbend': 0.6,
                    'Zrmax': 1.0, 'p': 0.4}, 
        'Apples, Cherries, Pears': {'Kcini': 0.8, 'Kcmid': 1.2, 
                                    'Kcend': 0.85, 'h': 4.0, 
                                    'Kcbini': 0.75, 'Kcbmid': 1.15, 
                                    'Kcbend': 0.8, 'Zrmax': 1.0, 
                                    'p': 0.5}, 
        'Apricots, Peaches, Stone Fruit': {'Kcini': 0.8, 'Kcmid': 1.15, 
                                            'Kcend': 0.85, 'h': 3.0, 
                                            'Kcbini': 0.75, 'Kcbmid': 1.1, 
                                            'Kcbend': 0.8, 'Zrmax': 1.0, 
                                            'p': 0.5}, 
        'Avocado': {'Kcini': 0.6, 'Kcmid': 0.85, 'Kcend': 0.75, 'h': 3.0, 
                    'Kcbini': 0.5, 'Kcbmid': 0.8, 'Kcbend': 0.7, 
                    'Zrmax': 0.5, 'p': 0.7}, 
        'Citrus': {'Kcini': 0.75, 'Kcmid': 0.7, 'Kcend': 0.75, 'h': 4.0, 
                    'Kcbini': 0.75, 'Kcbmid': 0.7, 'Kcbend': 0.75, 
                    'Zrmax': 1.2, 'p': 0.5}, 
        'Conifer Trees': {'Kcini': 1.0, 'Kcmid': 1, 'Kcend': 1.0, 
                          'h': 10.0, 'Kcbini': 0.95, 'Kcbmid': 0.95, 
                          'Kcbend': 0.95, 'Zrmax': 1.0, 'p': 0.7}, 
        'Kiwi': {'Kcini': 0.4, 'Kcmid': 1.05, 'Kcend': 1.05, 'h': 3.0, 
                 'Kcbini': 0.2, 'Kcbmid': 1.0, 'Kcbend': 1.0, 
                 'Zrmax': 0.7, 'p': 0.35}, 
        'Olives': {'Kcini': 0.65, 'Kcmid': 0.7, 'Kcend': 0.7, 'h': 3.0, 
                   'Kcbini': 0.55, 'Kcbmid': 0.65, 'Kcbend': 0.65, 
                   'Zrmax': 1.2, 'p': 0.65}, 
        'Pistachios': {'Kcini': 0.4, 'Kcmid': 1.1,'Kcend': 0.45, 
                       'h': 3.0, 'Kcbini': 0.2, 'Kcbmid': 1.05, 
                       'Kcbend': 0.4, 'Zrmax': 1.0, 'p': 0.4}, 
        'Walnut Orchard': {'Kcini': 0.5, 'Kcmid': 1.1, 'Kcend': 0.65, 
                           'h': 4.0, 'Kcbini': 0.4, 'Kcbmid': 1.05, 
                           'Kcbend': 0.6, 'Zrmax': 1.7, 'p': 0.5}}
      
