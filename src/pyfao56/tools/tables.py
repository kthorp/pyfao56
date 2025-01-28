"""
########################################################################
The tables.py module includes the FAO56Tables class, which contains
suggested values for attributes of the Parameters class as defined in
FAO-56, specifically in Tables 11, 12, 17, and 22 of FAO-56.

FAO-56 Table 11 - Lengths of crop development stages
FAO-56 Table 12 - Single crop coefficients (Kc)
FAO-56 Table 17 - Basal crop coefficients (Kcb)
FAO-56 Table 22 - Maximum root depth (Zr) and depletion fraction (p)

The tables.py module contains the following:
    FAO56Tables - A class for specifying parameter values as defined in
                  FAO-56 tables.

12/12/2024 FAOTables class created by Reagan Ames and Tyler Pokoski
01/08/2025 Modification for release by Kelly Thorp
########################################################################
"""

import pandas as pd
import io

class FAO56Tables:
    """A class for specifying parameter values from FAO-56 tables

    Attributes
    ----------
    table11 : Dataframe
        FAO-56 Table 11 data as str
        index - row number as int
        columns - ['Crop','Lini','Ldev','Lmid','Llate','Total',
                   'Plant Date','Region']
            Crop       - Crop description
            Lini       - Length Stage Initial (days)
            Ldev       - Length Stage Development (days)
            Lmid       - Length Stage Mid (days)
            Llate      - Length Stage End (days)
            Total      - Length growing season (days)
            Plant Date - Month of planting
            Region     - Growing location
    table12 : DataFrame
        FAO-56 Table 12 data as str
        index - row number as int
        columns - ['Crop','Kcini','Kcmid','Kcend','hmax']
            Crop  - Crop description
            Kcini - Kc Initial
            Kcmid - Kc Mid
            Kcend - Kc End
            hmax  - Plant Height Maximum (m)
    table17 : DataFrame
        FAO-56 Table 17 data as str
        index - row number as int
        columns - ['Crop','Kcbini','Kcbmid','Kcbend']
            Crop   - Crop description
            Kcbini - Kcb Initial
            Kcbmid - Kcb Mid
            Kcbend - Kcb End
    table22 : DataFrame
        FAO-56 Table 22 data as str
        index - row number as int
        columns - ['Crop','Zrmax1','Zrmax2','pbase']
            Crop   - Crop description
            Zrmax1 - Rooting depth maximum 1 (m)
            Zrmax2 - Rooting depth maximum 2 (m)
            pbase  - Depletion fraction
    synonyms : dict
        keys - common synonyms for crop names and other search terms
        values - list of corresponding  search terms in tables

    Methods
    -------
    search11(phrase,usesyn=True)
        Search FAO-56 Table 11 based on search phrase and synonym list
    search12(phrase,usesyn=True)
        Search FAO-56 Table 12 based on search phrase and synonym list
    search17(phrase,usesyn=True)
        Search FAO-56 Table 17 based on search phrase and synonym list
    search22(phrase,usesyn=True)
        Search FAO-56 Table 22 based on search phrase and synonym list
    """

    def __init__(self):
        """Initialize the FAO56Tables class attributes."""

        #FAO-56 Table 11. Lengths of crop development stages for various planting periods and climatic regions (days)
        #   Crop                         ,Lini,Ldev,Lmid,Llate,Total, Plant Date      , Region
        table11data = """
            broccoli                     ,  35,  45,  40,   15,  135, sep             , california desert usa
            cabbage                      ,  40,  60,  50,   15,  165, sep             , california desert usa
            carrots                      ,  20,  30,  30,   20,  100, oct jan         , arid climate
            carrots                      ,  30,  40,  60,   20,  150, feb mar         , mediterranean
            carrots                      ,  30,  50,  90,   30,  200, oct             , california desert usa
            cauliflower                  ,  35,  50,  40,   15,  140, sep             , california desert usa
            celery                       ,  25,  40,  95,   20,  180, oct             , semiarid
            celery                       ,  25,  40,  45,   15,  125, apr             , mediterranean
            celery                       ,  30,  55, 105,   20,  210, jan             , semiarid
            crucifers                    ,  20,  30,  20,   10,   80, apr             , mediterranean
            crucifers                    ,  25,  35,  25,   10,   95, feb             , mediterranean
            crucifers                    ,  30,  35,  90,   40,  195, oct nov         , mediterranean
            lettuce                      ,  20,  30,  15,   10,   75, apr             , mediterranean
            lettuce                      ,  30,  40,  25,   10,  105, nov jan         , mediterranean
            lettuce                      ,  25,  35,  30,   10,  100, oct nov         , arid region
            lettuce                      ,  35,  50,  45,   10,  140, feb             , mediterranean
            onion dry                    ,  15,  25,  70,   40,  150, apr             , mediterranean
            onion dry                    ,  20,  35, 110,   45,  210, oct jan         , arid region california
            onion green                  ,  25,  30,  10,    5,   70, apr may         , mediterranean
            onion green                  ,  20,  45,  20,   10,   95, oct             , arid region
            onion green                  ,  30,  55,  55,   40,  180, mar             , california usa
            onion seed                   ,  20,  45, 165,   45,  275, sep             , california desert usa
            spinach                      ,  20,  20,  20,    5,   65, apr sep oct     , mediterranean
            spinach                      ,  20,  30,  40,   10,  100, nov             , arid region
            radish                       ,   5,  10,  15,    5,   35, mar apr         , mediterranean europe
            radish                       ,  10,  10,  15,    5,   40, winter          , arid region
            eggplant                     ,  30,  40,  40,   20,  130, oct             , arid region
            eggplant                     ,  30,  45,  40,   25,  140, may jun         , mediterranean
            sweet peppers bell           ,  30,  35,  40,   20,  125, apr jun         , europe mediterranean
            sweet peppers bell           ,  30,  40, 110,   30,  210, oct             , arid region
            tomato                       ,  30,  40,  40,   25,  135, jan             , arid region
            tomato                       ,  35,  40,  50,   30,  155, apr may         , california usa
            tomato                       ,  25,  40,  60,   30,  155, jan             , california desert usa
            tomato                       ,  35,  45,  70,   30,  180, oct nov         , arid region
            tomato                       ,  30,  40,  45,   30,  145, apr may         , mediterranean
            cantaloupe                   ,  30,  45,  35,   10,  120, jan             , california usa
            cantaloupe                   ,  10,  60,  25,   25,  120, aug             , california usa
            cucumber                     ,  20,  30,  40,   15,  105, june aug        , arid region
            cucumber                     ,  25,  35,  50,   20,  130, nov feb         , arid region
            pumpkin winter squash        ,  20,  30,  30,   20,  100, mar aug         , mediterranean
            pumpkin winter squash        ,  25,  35,  35,   25,  120, jun             , europe
            squash zucchini              ,  25,  35,  25,   15,  100, apr dec         , mediterranean arid region
            squash zucchini              ,  20,  30,  25,   15,   90, may jun         , mediterranean europe
            sweet melons                 ,  25,  35,  40,   20,  120, may             , mediterranean
            sweet melons                 ,  30,  30,  50,   30,  140, mar             , california usa
            sweet melons                 ,  15,  40,  65,   15,  135, aug             , california desert usa
            sweet melons                 ,  30,  45,  65,   20,  160, dec jan         , arid region
            water melons                 ,  20,  30,  30,   30,  110, apr             , italy
            water melons                 ,  10,  20,  20,   30,   80, may aug         , near east desert
            beets table                  ,  15,  25,  20,   10,   70, apr may         , mediterranean
            beets table                  ,  25,  30,  25,   10,   90, feb mar         , mediterranean arid
            cassava year 1               ,  20,  40,  90,   60,  210, rainy season    , tropical regions
            cassava year 2               , 150,  40, 110,   60,  360, rainy season    , tropical regions
            potato                       ,  25,  30,  40,   30,  125, jan nov         , semiarid climate
            potato                       ,  25,  30,  45,   30,  130, may             , continental climate
            potato                       ,  30,  35,  50,   30,  145, apr             , europe
            potato                       ,  45,  30,  70,   20,  165, apr may         , idaho usa
            potato                       ,  30,  35,  50,   25,  140, dec             , california desert usa
            sweet potato                 ,  20,  30,  60,   40,  150, apr             , mediterranean
            sweet potato                 ,  15,  30,  50,   30,  125, rainy season    , tropical regions
            sugarbeet                    ,  30,  45,  90,   15,  180, mar             , california usa
            sugarbeet                    ,  25,  30,  90,   10,  155, jun             , california usa
            sugarbeet                    ,  25,  65, 100,   65,  255, sep             , california desert usa
            sugarbeet                    ,  50,  40,  50,   40,  180, apr             , idaho usa
            sugarbeet                    ,  25,  35,  50,   50,  160, may             , mediterranean
            sugarbeet                    ,  45,  75,  80,   30,  230, nov             , mediterranean
            sugarbeet                    ,  35,  60,  70,   40,  205, nov             , arid regions
            beans green                  ,  20,  30,  30,   10,   90, feb mar         , california mediterranean
            beans green                  ,  15,  25,  25,   10,   75, aug sep         , california egypt lebanon
            beans dry                    ,  20,  30,  40,   20,  110, may jun         , continental climates
            beans dry                    ,  15,  25,  35,   20,   95, jun             , pakistan california
            beans dry                    ,  25,  25,  30,   20,  100, jun             , idaho usa
            faba bean broad              ,  15,  25,  35,   15,   90, may             , europe
            faba bean broad              ,  20,  30,  35,   15,  100, mar apr         , mediterranean
            faba bean broad dry          ,  90,  45,  40,   60,  235, nov             , europe
            faba bean broad green        ,  90,  45,  40,    0,  175, nov             , europe
            green gram cowpeas           ,  20,  30,  30,   20,  110, mar             , mediterranean
            groundnut                    ,  25,  35,  45,   25,  130, dry season      , west africa
            groundnut                    ,  35,  35,  35,   35,  140, may             , high latitudes
            groundnut                    ,  35,  45,  35,   25,  140, may jun         , mediterranean
            lentil                       ,  20,  30,  60,   40,  150, apr             , europe
            lentil                       ,  25,  35,  70,   40,  170, oct nov         , arid region
            peas                         ,  15,  25,  35,   15,   90, may             , europe
            peas                         ,  20,  30,  35,   15,  100, mar apr         , mediterranean
            peas                         ,  35,  25,  30,   20,  110, apr             , idaho usa
            soybeans                     ,  15,  15,  40,   15,   85, dec             , tropics
            soybeans                     ,  20,  35,  60,   25,  140, may             , central usa
            soybeans                     ,  20,  25,  75,   30,  150, jun             , japan
            artichoke                    ,  40,  40, 250,   30,  360, apr first year  , california
            artichoke                    ,  20,  25, 250,   30,  325, may second year , california
            asparagus                    ,  50,  30, 100,   50,  230, feb             , warm winter
            asparagus                    ,  90,  30, 200,   45,  365, feb             , mediterranean
            cotton                       ,  30,  50,  60,   55,  195, mar may         , egypt pakistan california
            cotton                       ,  45,  90,  45,   45,  225, mar             , california desert usa
            cotton                       ,  30,  50,  60,   55,  195, sep             , yemen
            cotton                       ,  30,  50,  55,   45,  180, apr             , texas
            flax                         ,  25,  35,  50,   40,  150, apr             , europe
            flax                         ,  30,  40, 100,   50,  220, oct             , arizona
            castor beans                 ,  25,  40,  65,   50,  180, mar             , semiarid climates
            castor beans                 ,  20,  40,  50,   25,  135, nov             , indonesia
            safflower                    ,  20,  35,  45,   25,  125, apr             , california usa
            safflower                    ,  25,  35,  55,   30,  145, mar             , high latitudes
            safflower                    ,  35,  55,  60,   40,  190, oct nov         , arid region
            sesame                       ,  20,  30,  40,   20,  100, jun             , china
            sunflower                    ,  25,  35,  45,   25,  130, apr may         , mediterranean california
            barley oats wheat            ,  15,  25,  50,   30,  120, nov             , central india
            barley oats wheat            ,  20,  25,  60,   30,  135, mar apr         , 35-45 degrees latitude
            barley oats wheat            ,  15,  30,  65,   40,  150, jul             , east africa
            barley oats wheat            ,  40,  30,  40,   20,  130, apr             , east africa
            barley oats wheat            ,  40,  60,  60,   40,  200, nov             , east africa
            barley oats wheat            ,  20,  50,  60,   30,  160, dec             , california desert usa
            winter wheat                 ,  20,  60,  70,   30,  180, dec             , california usa
            winter wheat                 ,  30, 140,  40,   30,  240, nov             , mediterranean
            winter wheat                 , 160,  75,  75,   25,  335, oct             , idaho usa
            grains small                 ,  20,  30,  60,   40,  150, apr             , mediterranean
            grains small                 ,  25,  35,  65,   40,  165, oct nov         , pakistan arid region
            maize grain                  ,  30,  50,  60,   40,  180, apr             , east africa
            maize grain                  ,  25,  40,  45,   30,  140, dec jan         , arid climate
            maize grain                  ,  20,  35,  40,   30,  125, jun             , nigeria humid
            maize grain                  ,  20,  35,  40,   30,  125, oct             , india dry cool
            maize grain                  ,  30,  40,  50,   30,  150, apr             , spain spring summer california
            maize grain                  ,  30,  40,  50,   50,  170, apr             , idaho usa
            maize sweet                  ,  20,  20,  30,   10,   80, mar             , philippines
            maize sweet                  ,  20,  25,  25,   10,   80, may jun         , mediterranean
            maize sweet                  ,  20,  30,  30,   10,   90, oct dec         , arid climate
            maize sweet                  ,  30,  30,  30,   10,  110, apr             , idaho usa
            maize sweet                  ,  20,  40,  70,   10,  140, jan             , california desert usa
            millet                       ,  15,  25,  40,   25,  105, jun             , pakistan
            millet                       ,  20,  30,  55,   35,  140, apr             , central usa
            sorghum                      ,  20,  35,  40,   30,  130, may june        , usa pakistan mediterranean
            sorghum                      ,  20,  35,  45,   30,  140, mar apr         , arid region
            rice                         ,  30,  30,  60,   30,  150, dec may         , tropics mediterranean
            rice                         ,  30,  30,  80,   40,  180, may             , tropics
            alfalfa total season         ,  10,  30,    ,     ,     ,                 , last -4oC in spring until first -4oC in fall
            alfalfa first cutting cycle  ,  10,  20,  20,   10,   60, jan             , california usa
            alfalfa first cutting cycle  ,  10,  30,  25,   10,   75, apr last -4oC   , idaho usa
            alfalfa other cutting cycles ,   5,  10,  10,    5,   30, mar             , california usa
            alfalfa other cutting cycles ,   5,  20,  10,   10,   45, jun             , idaho usa
            bermuda for seed             ,  10,  25,  35,   35,  105, mar             , california desert usa
            bermuda hay several cuttings ,  10,  15,  75,   35,  135,                 , california desert usa
            grass pasture                ,  10,  20,    ,     ,     ,                 , 7 days before last -4oC in spring until 7 days after first -4oC in fall
            sudan first cutting cycle    ,  25,  25,  15,   10,   75, apr             , california desert usa
            sudan other cutting cycles   ,   3,  15,  12,    7,   37, jun             , california desert usa
            sugarcane virgin             ,  35,  60, 190,  120,  405,                 , low latitudes
            sugarcane virgin             ,  50,  70, 220,  140,  480,                 , tropics
            sugarcane virgin             ,  75, 105, 330,  210,  720,                 , hawaii usa
            sugarcane ratoon             ,  25,  70, 135,   50,  280,                 , low latitudes
            sugarcane ratoon             ,  30,  50, 180,   60,  320,                 , tropics
            sugarcane ratoon             ,  35, 105, 210,   70,  420,                 , hawaii usa
            banana first year            , 120,  90, 120,   60,  390, mar             , mediterranean
            banana second year           , 120,  60, 180,    5,  365, feb             , mediterranean
            pineapple                    ,  60, 120, 600,   10,  790,                 , hawaii usa
            grapes                       ,  20,  40, 120,   60,  240, apr             , low latitudes
            grapes                       ,  20,  50,  75,   60,  205, mar             , california usa
            grapes                       ,  20,  50,  90,   20,  180, may             , high latitudes
            grapes                       ,  30,  60,  40,   80,  210, apr             , mid latitudes wine
            hops                         ,  25,  40,  80,   10,  155, apr             , idaho usa
            citrus                       ,  60,  90, 120,   95,  365, jan             , mediterranean
            deciduous orchard            ,  20,  70,  90,   30,  210, mar             , high latitudes
            deciduous orchard            ,  20,  70, 120,   60,  270, mar             , low latitudes
            deciduous orchard            ,  30,  50, 130,   30,  240, mar             , california usa
            olives                       ,  30,  90,  60,   90,  270, mar             , mediterranean
            pistachios                   ,  20,  60,  30,   40,  150, feb             , mediterranean
            walnuts                      ,  20,  10, 130,   30,  190, apr             , utah usa
            wetlands cattails bulrush    ,  10,  30,  80,   20,  140, may             , utah usa killing frost
            wetlands cattails bulrush    , 180,  60,  90,   35,  365, nov             , florida usa
            wetlands short vegetation    , 180,  60,  90,   35,  365, nov             , frost-free climate"""
        self.table11 = pd.read_csv(io.StringIO(table11data),
                                   names=['Crop','Lini','Ldev','Lmid','Llate','Total','Plant Date','Region'],
                                   dtype=str)
        for col in self.table11.columns:
            self.table11[col] = self.table11[col].str.strip()

        #FAO-56 Table 12. Single (time-averaged) crop coefficients, Kc, and mean maximum plant
        #heights for non stressed, well-managed crops in subhumid climates (RHmin=45%, u2=2m/s)
        #for use with the FAO Penman-Monteith ETo.
        #   Crop                                                          ,Kcini,Kcmid,Kcend,hmax
        table12data = """
            small vegetables                                              , 0.7 , 1.05, 0.95, 
            broccoli                                                      , 0.7 , 1.05, 0.95, 0.3
            brussel sprouts                                               , 0.7 , 1.05, 0.95, 0.4
            cabbage                                                       , 0.7 , 1.05, 0.95, 0.4
            carrots                                                       , 0.7 , 1.05, 0.95, 0.3
            cauliflower                                                   , 0.7 , 1.05, 0.95, 0.4
            celery                                                        , 0.7 , 1.05, 1.00, 0.6
            garlic                                                        , 0.7 , 1.00, 0.70, 0.3
            lettuce                                                       , 0.7 , 1.00, 0.95, 0.3
            onions dry                                                    , 0.7 , 1.05, 0.75, 0.4
            onions green                                                  , 0.7 , 1.00, 1.00, 0.3
            onions seed                                                   , 0.7 , 1.05, 0.80, 0.5
            spinach                                                       , 0.7 , 1.00, 0.95, 0.3
            radish                                                        , 0.7 , 0.90, 0.85, 0.3
            vegetables solanum family solanaceae                          , 0.6 , 1.15, 0.80, 
            eggplant                                                      , 0.6 , 1.05, 0.90, 0.8
            sweet peppers bell                                            , 0.6 , 1.05, 0.90, 0.7
            tomato                                                        , 0.6 , 1.15, 0.80, 0.6
            vegetables cucumber family cucurbitaceae                      , 0.5 , 1.00, 0.80, 
            cantaloupe                                                    , 0.5 , 0.85, 0.60, 0.3
            cucumber fresh market                                         , 0.6 , 1.00, 0.75, 0.3
            cucumber machine harvest                                      , 0.5 , 1.00, 0.90, 0.3
            pumpkin winter squash                                         , 0.5 , 1.00, 0.80, 0.4
            squash zucchini                                               , 0.5 , 0.95, 0.75, 0.3
            sweet melons                                                  , 0.5 , 1.05, 0.75, 0.4
            watermelon                                                    , 0.4 , 1.00, 0.75, 0.4
            roots tubers                                                  , 0.5 , 1.10, 0.95, 
            beets table                                                   , 0.5 , 1.05, 0.95, 0.4
            cassava year 1                                                , 0.3 , 0.80, 0.30, 1.0
            cassava year 2                                                , 0.3 , 1.10, 0.50, 1.5
            parsnip                                                       , 0.5 , 1.05, 0.95, 0.4
            potato                                                        , 0.5 , 1.15, 0.75, 0.6
            sweet potato                                                  , 0.5 , 1.15, 0.65, 0.4
            turnip rutabaga                                               , 0.5 , 1.10, 0.95, 0.6
            sugar beet                                                    , 0.35, 1.20, 0.70, 0.5
            legumes leguminosae                                           , 0.4 , 1.15, 0.55, 
            beans green                                                   , 0.5 , 1.05, 0.90, 0.4
            beans dry pulses                                              , 0.4 , 1.15, 0.35, 0.4
            chickpea                                                      , 0.4 , 1.00, 0.35, 0.4
            faba bean broad fresh                                         , 0.5 , 1.15, 1.10, 0.8
            faba bean broad dry seed                                      , 0.5 , 1.15, 0.30, 0.8
            garbanzo                                                      , 0.4 , 1.15, 0.35, 0.8
            green gram cowpeas harvested fresh                            , 0.4 , 1.05, 0.60, 0.4
            green gram cowpeas harvested dry                              , 0.4 , 1.05, 0.35, 0.4
            groundnut peanut                                              , 0.4 , 1.15, 0.60, 0.4
            lentil                                                        , 0.4 , 1.10, 0.30, 0.5
            peas fresh                                                    , 0.5 , 1.15, 1.10, 0.5
            peas dry seed                                                 , 0.5 , 1.15, 0.30, 0.5
            soybeans                                                      , 0.5 , 1.15, 0.50, 0.75
            perennial vegetables winter dormancy bare mulched soil        , 0.5 , 1.00, 0.80, 
            artichokes                                                    , 0.5 , 1.00, 0.95, 0.7
            asparagus                                                     , 0.5 , 0.95, 0.30, 0.5
            mint                                                          , 0.60, 1.15, 1.10, 0.7
            strawberries                                                  , 0.40, 0.85, 0.75, 0.2
            fiber crops                                                   , 0.35,     ,     , 
            cotton                                                        , 0.35, 1.17, 0.60, 1.35
            flax                                                          , 0.35, 1.10, 0.25, 1.2
            sisal                                                         , 0.35, 0.55, 0.55, 1.5
            oil crops                                                     , 0.35, 1.15, 0.35, 
            castorbean ricinus                                            , 0.35, 1.15, 0.55, 0.3
            rapeseed canola                                               , 0.35, 1.10, 0.35, 0.6
            safflower                                                     , 0.35, 1.10, 0.25, 0.8
            sesame                                                        , 0.35, 1.10, 0.25, 1.0
            sunflower                                                     , 0.35, 1.10, 0.35, 2.0
            cereals                                                       , 0.3 , 1.15, 0.4 , 
            barley                                                        , 0.3 , 1.15, 0.25, 1
            oats                                                          , 0.3 , 1.15, 0.25, 1
            spring wheat                                                  , 0.3 , 1.15, 0.25, 1
            winter wheat frozen soils                                     , 0.4 , 1.15, 0.25, 1
            winter wheat non-frozen soils                                 , 0.7 , 1.15, 0.25, 1
            maize field grain corn 18% moisture                           , 0.3 , 1.20, 0.35, 2
            maize field grain corn harvested wet                          , 0.3 , 1.20, 0.60, 2
            maize sweet corn fresh                                        , 0.3 , 1.15, 1.05, 1.5
            maize sweet corn dry                                          , 0.3 , 1.15, 0.35, 1.5
            millet                                                        , 0.3 , 1.00, 0.30, 1.5
            sorghum grain                                                 , 0.3 , 1.05, 0.55, 1.5
            sorgum sweet                                                  , 0.3 , 1.20, 1.05, 3
            rice                                                          , 1.05, 1.20, 0.75, 1
            alfalfa hay averaged cutting effects                          , 0.40, 0.95, 0.90, 0.7
            alfalfa hay individual cutting periods                        , 0.40, 1.20, 1.15, 0.7
            alfalfa for seed                                              , 0.40, 0.50, 0.50, 0.7
            bermuda hay averaged cutting effects                          , 0.55, 1.00, 0.85, 0.35
            bermuda hay spring crop for seed                              , 0.35, 0.90, 0.65, 0.4
            clover hay berseem averaged cutting effects                   , 0.40, 0.90, 0.85, 0.6
            clover hay individual cutting periods                         , 0.40, 1.15, 1.10, 0.6
            rye grass hay averaged cutting effects                        , 0.95, 1.05, 1.00, 0.3
            sudangrass hay annual averaged cutting effects                , 0.50, 0.90, 0.85, 1.2
            sudangrass individual cutting periods                         , 0.50, 1.15, 1.10, 1.2
            grazing pasture rotated                                       , 0.40, 0.90, 0.85, 0.22
            grazing pasture extensive                                     , 0.30, 0.75, 0.75, 0.10
            turfgrass cool season                                         , 0.90, 0.95, 0.95, 0.10
            turfgrass warm season                                         , 0.80, 0.85, 0.85, 0.10
            sugarcane                                                     , 0.40, 1.25, 0.75, 3
            banana first year                                             , 0.50, 1.10, 1.00, 3
            banana second year                                            , 1.00, 1.20, 1.10, 4
            cacao                                                         , 1.00, 1.05, 1.05, 3
            coffee bare ground cover                                      , 0.90, 0.95, 0.95, 2.5
            coffee with weeds                                             , 1.05, 1.10, 1.10, 2.5
            date palms                                                    , 0.90, 0.95, 0.95, 8
            palm trees                                                    , 0.95, 1.00, 1.00, 8
            pineapple bare soil                                           , 0.50, 0.30, 0.30, 0.9
            pineapple with grass cover                                    , 0.50, 0.50, 0.50, 0.9
            rubber trees                                                  , 0.95, 1.00, 1.00, 10
            tea non-shaded                                                , 0.95, 1.00, 1.00, 1.5
            tea shaded                                                    , 1.10, 1.15, 1.15, 2
            berries bushes                                                , 0.30, 1.05, 0.50, 1.5
            grapes table raisin                                           , 0.30, 0.85, 0.45, 2
            grapes wine                                                   , 0.30, 0.70, 0.45, 1.75
            hops                                                          , 0.3 , 1.05, 0.85, 5
            almonds no ground cover                                       , 0.40, 0.90, 0.65, 5
            apples cherries pears no ground cover killing frost           , 0.45, 0.95, 0.70, 4
            apples cherries pears no ground cover no frosts               , 0.60, 0.95, 0.75, 4
            apples cherries pears active ground cover killing frost       , 0.50, 1.20, 0.95, 4
            apples cherries pears active ground cover no frosts           , 0.80, 1.20, 0.85, 4
            apricots peaches stone fruit no ground cover killing frost    , 0.45, 0.90, 0.65, 3
            apricots peaches stone fruit no ground cover no frosts        , 0.55, 0.90, 0.65, 3
            apricots peaches stone fruit active ground cover killing frost, 0.50, 1.15, 0.90, 3
            apricots peaches stone fruit active ground cover no frosts    , 0.80, 1.15, 0.85, 3
            avocado no ground cover                                       , 0.60, 0.85, 0.75, 3
            citrus no ground cover 70% canopy                             , 0.70, 0.65, 0.70, 4
            citrus no ground cover 50% canopy                             , 0.65, 0.60, 0.65, 3
            citrus no ground cover 20% canopy                             , 0.50, 0.45, 0.55, 2
            citrus active ground cover or weeds 70% canopy                , 0.75, 0.70, 0.75, 4
            citrus active ground cover or weeds 50% canopy                , 0.80, 0.80, 0.80, 3
            citrus active ground cover or weeds 20% canopy                , 0.85, 0.85, 0.85, 2
            conifer trees                                                 , 1.00, 1.00, 1.00, 10
            kiwi                                                          , 0.40, 1.05, 1.05, 3
            olives 40% to 60% ground coverage by canopy                   , 0.65, 0.70, 0.70, 4
            pistachios no ground cover                                    , 0.40, 1.10, 0.45, 4
            walnut orchard                                                , 0.50, 1.10, 0.65, 4.5
            cattails bulrushes killing frost                              , 0.30, 1.20, 0.30, 2
            cattails bulrushes no frost                                   , 0.60, 1.20, 0.60, 2
            short vegetation no frost                                     , 1.05, 1.10, 1.10, 0.3
            reed swamp standing water                                     , 1.00, 1.20, 1.00, 2
            reed swamp moist soil                                         , 0.90, 1.20, 0.70, 2
            open water < 2 m depth or in subhumid climates or tropics     ,     , 1.05, 1.05, 
            open water > 5 m depth clear of turbidity temperate climate   ,     , 0.65, 1.25,  """
        self.table12 = pd.read_csv(io.StringIO(table12data),
                                   names=['Crop','Kcini','Kcmid','Kcend','hmax'],
                                   dtype=str)
        for col in self.table12.columns:
            self.table12[col] = self.table12[col].str.strip()

        #FAO-56 Table 17. Basal crop coefficients, Kcb, for non stressed, well-managed crops in
        #subhumid climates (RHmin = 45%, u2 = 2 m/s) for use with the FAO Penman-Montieth ETo
        #   Crop                                                          Kcbini,Kcbmid,Kcbend
        table17data = """
            small vegetables                                              , 0.15,  0.95,  0.85
            broccoli                                                      , 0.15,  0.95,  0.85
            brussel sprouts                                               , 0.15,  0.95,  0.85
            cabbage                                                       , 0.15,  0.95,  0.85
            carrots                                                       , 0.15,  0.95,  0.85
            cauliflower                                                   , 0.15,  0.95,  0.85
            celery                                                        , 0.15,  0.95,  0.90
            garlic                                                        , 0.15,  0.90,  0.60
            lettuce                                                       , 0.15,  0.90,  0.90
            onions dry                                                    , 0.15,  0.95,  0.65
            onions green                                                  , 0.15,  0.90,  0.90
            onions seed                                                   , 0.15,  1.05,  0.70
            spinach                                                       , 0.15,  0.90,  0.85
            radishes                                                      , 0.15,  0.85,  0.75
            vegetables solanum family solanaceae                          , 0.15,  1.10,  0.70
            eggplant                                                      , 0.15,  1.00,  0.80
            sweet peppers bell                                            , 0.15,  1.00,  0.80
            tomato                                                        , 0.15,  1.10,  0.70
            vegetables cucumber family cucurbitaceae                      , 0.15,  0.95,  0.70
            cantaloupe                                                    , 0.15,  0.75,  0.50
            cucumber fresh market                                         , 0.15,  0.95,  0.70
            cucumber machine harvest                                      , 0.15,  0.95,  0.80
            pumpkin winter squash                                         , 0.15,  0.95,  0.70
            squash zucchini                                               , 0.15,  0.90,  0.70
            sweet melons                                                  , 0.15,  1.00,  0.70
            watermelon                                                    , 0.15,  0.95,  0.70
            roots tubers                                                  , 0.15,  1.00,  0.85
            beets table                                                   , 0.15,  0.95,  0.85
            cassava year 1                                                , 0.15,  0.70,  0.20
            cassava year 2                                                , 0.15,  1.00,  0.45
            parsnip                                                       , 0.15,  0.95,  0.85
            potato                                                        , 0.15,  1.10,  0.65
            sweet potato                                                  , 0.15,  1.10,  0.55
            turnip rutabaga                                               , 0.15,  1.00,  0.85
            sugar beet                                                    , 0.15,  1.15,  0.50
            legumes leguminosae                                           , 0.15,  1.10,  0.50
            beans green                                                   , 0.15,  1.00,  0.80
            beans dry pulses                                              , 0.15,  1.10,  0.25
            chickpea                                                      , 0.15,  0.95,  0.25
            faba bean broad fresh                                         , 0.15,  1.10,  1.05
            faba bean dry seed                                            , 0.15,  1.10,  0.20
            garbanzo                                                      , 0.15,  1.05,  0.25
            green gram cowpeas fresh                                      , 0.15,  1.00,  0.55
            green gram cowpeas dry                                        , 0.15,  1.00,  0.25
            groundnut peanut                                              , 0.15,  1.10,  0.50
            lentil                                                        , 0.15,  1.05,  0.20
            peas fresh                                                    , 0.15,  1.10,  1.05
            peas dry seed                                                 , 0.15,  1.10,  0.20
            soybeans                                                      , 0.15,  1.10,  0.30
            artichokes                                                    , 0.15,  0.95,  0.90
            asparagus                                                     , 0.15,  0.90,  0.20
            mint                                                          , 0.40,  1.10,  1.05
            strawberries                                                  , 0.30,  0.80,  0.70
            fiber crops                                                   , 0.15,      , 
            cotton                                                        , 0.15,  1.12,  0.45
            flax                                                          , 0.15,  1.05,  0.20
            sisal                                                         , 0.15,  0.55,  0.55
            oil crops                                                     , 0.15,  1.10,  0.25
            castorbean ricinus                                            , 0.15,  1.10,  0.45
            rapeseed canola                                               , 0.15,  1.10,  0.25
            safflower                                                     , 0.15,  1.10,  0.20
            sesame                                                        , 0.15,  1.05,  0.20
            sunflower                                                     , 0.15,  1.10,  0.25
            cereals                                                       , 0.15,  1.10,  0.25
            barley                                                        , 0.15,  1.10,  0.15
            oats                                                          , 0.15,  1.10,  0.15
            spring wheat                                                  , 0.15,  1.10,  0.15
            winter wheat                                                  , 0.15,  1.10,  0.15
            maize field grain corn 18% moisture                           , 0.15,  1.15,  0.15
            maize field grain corn harvested wet                          , 0.15,  1.15,  0.50
            maize sweet corn fresh                                        , 0.15,  1.10,  1.00
            maize sweet corn dry                                          , 0.15,  1.10,  0.15
            millet                                                        , 0.15,  0.95,  0.20
            sorghum grain                                                 , 0.15,  1.00,  0.35
            sorghum sweet                                                 , 0.15,  1.15,  1.00
            rice                                                          , 1.00,  1.15,  0.57
            alfalfa hay individual cutting periods                        , 0.30,  1.15,  1.10
            alfalfa hay for seed                                          , 0.30,  0.45,  0.45
            bermuda hay averaged cutting effects                          , 0.50,  0.95,  0.80
            bermuda hay spring crop for seed                              , 0.15,  0.85,  0.60
            clover hay berseem individual cutting periods                 , 0.30,  1.10,  1.05
            rye grass hay averaged cutting effects                        , 0.85,  1.00,  0.95
            sudangrass hay annual individual cutting periods              , 0.30,  1.10,  1.05
            grazing pasture rotated grazing                               , 0.30,  0.90,  0.80
            grazing pasture extensive grazing                             , 0.30,  0.70,  0.70
            turfgrass cool season                                         , 0.85,  0.90,  0.90
            turfgrass warm season                                         , 0.75,  0.80,  0.80
            sugarcane                                                     , 0.15,  1.20,  0.70
            banana first year                                             , 0.15,  1.05,  0.90
            banana second year                                            , 0.60,  1.10,  1.05
            cacao                                                         , 0.90,  1.00,  1.00
            coffee bare ground cover                                      , 0.80,  0.90,  0.90
            coffee with weeds                                             , 1.00,  1.05,  1.05
            date palms                                                    , 0.80,  0.85,  0.85
            palm trees                                                    , 0.85,  0.90,  0.90
            pineapple multiyear crop bare soil                            , 0.15,  0.25,  0.25
            pineapple multiyear crop with grass cover                     , 0.30,  0.45,  0.45
            rubber trees                                                  , 0.85,  0.90,  0.90
            tea nonshaded                                                 , 0.90,  0.95,  0.90
            tea shaded                                                    , 1.00,  1.10,  1.05
            berries bushes                                                , 0.20,  1.00,  0.40
            grapes table raisin                                           , 0.15,  0.80,  0.40
            grapes wine                                                   , 0.15,  0.65,  0.40
            hops                                                          , 0.15,  1.00,  0.80
            almonds no ground cover                                       , 0.20,  0.85,  0.60
            apples cherries pears no ground cover killing frost           , 0.35,  0.90,  0.65
            apples cherries pears no ground cover no frosts               , 0.50,  0.90,  0.70
            apples cherries pears active ground cover killing frost       , 0.45,  1.15,  0.90
            apples cherries pears active ground cover no frosts           , 0.75,  1.15,  0.80
            apricots peaches stone fruit no ground cover killing frost    , 0.35,  0.85,  0.60
            apricots peaches stone fruit no ground cover no frosts        , 0.45,  0.85,  0.60
            apricots peaches stone fruit active ground cover killing frost, 0.45,  1.10,  0.85
            apricots peaches stone fruit active ground cover no frosts    , 0.75,  1.10,  0.80
            avocado no ground cover                                       , 0.50,  0.80,  0.70
            citrus no ground cover 70% canopy                             , 0.65,  0.60,  0.65
            citrus no ground cover 50% canopy                             , 0.60,  0.55,  0.60
            citrus no ground cover 20% canopy                             , 0.45,  0.40,  0.50
            citrus with active ground cover or weeds 70% canopy           , 0.75,  0.70,  0.75
            citrus with active ground cover or weeds 50% canopy           , 0.75,  0.75,  0.75
            citrus with active ground cover or weeds 20% canopy           , 0.80,  0.80,  0.85
            conifer trees                                                 , 0.95,  0.95,  0.95
            kiwi                                                          , 0.20,  1.00,  1.00
            olives 40% to 60% ground coverage by canopy                   , 0.55,  0.65,  0.65
            pistachios no ground cover                                    , 0.20,  1.05,  0.40
            walnut orchard                                                , 0.40,  1.05,  0.60"""
        self.table17 = pd.read_csv(io.StringIO(table17data),
                                   names=['Crop','Kcbini','Kcbmid','Kcbend'],
                                   dtype=str)
        for col in self.table17.columns:
            self.table17[col] = self.table17[col].str.strip()

        #FAO-56 Table 22. Ranges of maximum effective rooting depth (Zr)
        #and soil water depletion fraction for no stress (p) for common
        #crops
        #   Crop                                      Zrmax1,Zrmax2,pbase
        table22data = """
            broccoli                                   , 0.4,   0.6, 0.45
            brussel sprouts                            , 0.4,   0.6, 0.45
            cabbage                                    , 0.5,   0.8, 0.45
            carrots                                    , 0.5,   1.0, 0.35
            cauliflower                                , 0.4,   0.7, 0.45
            celery                                     , 0.3,   0.5, 0.20
            garlic                                     , 0.3,   0.5, 0.30
            lettuce                                    , 0.3,   0.5, 0.30
            onions dry                                 , 0.3,   0.6, 0.30
            onoins green                               , 0.3,   0.6, 0.30
            onions seed                                , 0.3,   0.6, 0.35
            spinach                                    , 0.3,   0.5, 0.20
            radishes                                   , 0.3,   0.5, 0.30
            eggplant                                   , 0.7,   1.2, 0.45
            sweet peppers bell                         , 0.5,   1.0, 0.30
            tomato                                     , 0.7,   1.5, 0.40
            cantaloupe                                 , 0.9,   1.5, 0.45
            cucumber fresh market                      , 0.7,   1.2, 0.50
            cucumber machine harvest                   , 0.7,   1.2, 0.50
            pumpkin winter squash                      , 1.0,   1.5, 0.35
            squash zucchini                            , 0.6,   1.0, 0.50
            sweet melons                               , 0.8,   1.5, 0.40
            watermelon                                 , 0.8,   1.5, 0.40
            beets table                                , 0.6,   1.0, 0.50
            cassava year 1                             , 0.5,   0.8, 0.35
            cassava year 2                             , 0.7,   1.0, 0.40
            parsnip                                    , 0.5,   1.0, 0.40
            potato                                     , 0.4,   0.6, 0.35
            sweet potato                               , 1.0,   1.5, 0.65
            turnip rutabaga                            , 0.5,   1.0, 0.50
            sugar beet                                 , 0.7,   1.2, 0.55
            beans green                                , 0.5,   0.7, 0.45
            beans dry pulses                           , 0.6,   0.9, 0.45
            beans lima large vines                     , 0.8,   1.2, 0.45
            chickpea                                   , 0.6,   1.0, 0.50
            faba bean broad fresh                      , 0.5,   0.7, 0.45
            faba bean broad dry seed                   , 0.5,   0.7, 0.45
            garbanzo                                   , 0.6,   1.0, 0.45
            green gram cowpeas                         , 0.6,   1.0, 0.45
            groundnut peanut                           , 0.5,   1.0, 0.50
            lentil                                     , 0.6,   0.8, 0.50
            peas fresh                                 , 0.6,   1.0, 0.35
            peas dry seed                              , 0.6,   1.0, 0.40
            soybeans                                   , 0.6,   1.3, 0.50
            artichokes                                 , 0.6,   0.9, 0.45
            asparagus                                  , 1.2,   1.8, 0.45
            mint                                       , 0.4,   0.8, 0.40
            strawberries                               , 0.2,   0.3, 0.20
            cotton                                     , 1.0,   1.7, 0.65
            flax                                       , 1.0,   1.5, 0.50
            sisal                                      , 0.5,   1.0, 0.80
            castorbean ricinus                         , 1.0,   2.0, 0.50
            rapeseed canola                            , 1.0,   1.5, 0.60
            safflower                                  , 1.0,   2.0, 0.60
            sesame                                     , 1.0,   1.5, 0.60
            sunflower                                  , 0.8,   1.5, 0.45
            barley                                     , 1.0,   1.5, 0.55
            oats                                       , 1.0,   1.5, 0.55
            spring wheat                               , 1.0,   1.5, 0.55
            winter wheat                               , 1.5,   1.8, 0.55
            maize field grain corn                     , 1.0,   1.7, 0.55
            maize sweet corn                           , 0.8,   1.2, 0.50
            millet                                     , 1.0,   2.0, 0.55
            sorghum grain                              , 1.0,   2.0, 0.55
            sorghum sweet                              , 1.0,   2.0, 0.50
            rice                                       , 0.5,   1.0, 0.20
            alfalfa for hay                            , 1.0,   2.0, 0.55
            alfalfa for seed                           , 1.0,   3.0, 0.60
            bermuda for hay                            , 1.0,   1.5, 0.55
            spring crop for seed                       , 1.0,   1.5, 0.60
            clover hay berseem                         , 0.6,   0.9, 0.50
            rye grass hay                              , 0.6,   1.0, 0.60
            sudangrass hay annual                      , 1.0,   1.5, 0.55
            grazing pasture rotated                    , 0.5,   1.5, 0.60
            grazing pasture extensive                  , 0.5,   1.5, 0.60
            turfgrass cool season                      , 0.5,   1.0, 0.40
            turfgrass warm season                      , 0.5,   1.0, 0.50
            sugarcane                                  , 1.2,   2.0, 0.65
            banana first year                          , 0.5,   0.9, 0.35
            banana second year                         , 0.5,   0.9, 0.35
            cacao                                      , 0.7,   1.0, 0.30
            coffee                                     , 0.9,   1.5, 0.40
            date palms                                 , 1.5,   2.5, 0.50
            palm trees                                 , 0.7,   1.1, 0.65
            pineapple                                  , 0.3,   0.6, 0.50
            rubber trees                               , 1.0,   1.5, 0.40
            tea non-shaded                             , 0.9,   1.5, 0.40
            tea shaded                                 , 0.9,   1.5, 0.45
            berries bushes                             , 0.6,   1.2, 0.50
            grapes table raisin                        , 1.0,   2.0, 0.35
            grapes wine                                , 1.0,   2.0, 0.45
            hops                                       , 1.0,   1.2, 0.50
            almonds                                    , 1.0,   2.0, 0.40
            apples cherries pears                      , 1.0,   2.0, 0.50
            apricots peaches stone fruit               , 1.0,   2.0, 0.50
            avocado                                    , 0.5,   1.0, 0.70
            citrus 70% canopy                          , 1.2,   1.5, 0.50
            citrus 50% canopy                          , 1.1,   1.5, 0.50
            citrus 20% canopy                          , 0.8,   1.1, 0.50
            conifer trees                              , 1.0,   1.5, 0.70
            kiwi                                       , 0.7,   1.3, 0.35
            olives 40% to 60% ground coverage by canopy, 1.2,   1.7, 0.65
            pistachios                                 , 1.0,   1.5, 0.40
            walnut orchard                             , 1.7,   2.4, 0.50"""
        self.table22 = pd.read_csv(io.StringIO(table22data),
                                   names=['Crop','Zrmax1','Zrmax2','pbase'],
                                   dtype=str)
        for col in self.table22.columns:
            self.table22[col] = self.table22[col].str.strip()

        self.synonyms = {
            "brussel sprouts": ["crucifers"],
            "brussel sprout": ["crucifers"],
            "red cabbage": ["cabbage","crucifers"],
            "green cabbage": ["cabbage","crucifers"],
            "purple cabbage": ["cabbage","crucifers"],
            "savoy cabbage": ["cabbage","crucifers"],
            "cabbages": ["cabbage","crucifers"],
            "elephant garlic": ["garlic"],
            "wild garlic": ["garlic"],
            "single clove garlic": ["garlic"],
            "romaine lettuce": ["lettuce"],
            "romaine": ["lettuce"],
            "onions": ["onion"],
            "red radish": ["radish"],
            "green radish": ["radish"],
            "black radish": ["radish"],
            "oilseed radish": ["radish"],
            "wild radish": ["radish"],
            "daikon": ["radish"],
            "radishes": ["radish"],
            "egg plant": ["eggplant"],
            "garden egg": ["eggplant"],
            "eggplants": ["eggplant"],
            "egg plants": ["eggplant"],
            "bell pepper": ["sweet pepper"],
            "bell peppers": ["sweet pepper"],
            "paprika": ["sweet pepper"],
            "capsicus": ["sweet pepper"],
            "capsicum": ["sweet pepper"],
            "tomatoes": ["tomato"],
            "true cantaloupe": ["cantaloupe"],
            "european cantaloupe": ["cantaloupe"],
            "american cantaloupe": ["cantaloupe"],
            "cantaloupes": ["cantaloupe"],
            "muskmelon": ["cantaloupe"],
            "rockmelon": ["cantaloupe"],
            "spanspek": ["cantaloupe"],
            "cucumbers": ["cucumber"],
            "pumpkins": ["pumpkin"],
            "winter squashes": ["winter squash"],
            "kabocha": ["winter squash"],
            "butternut squash": ["winter squash"],
            "spaghetti squash": ["winter squash"],
            "delicata squash": ["winter squash"],
            "acorn squash": ["winter squash"],
            "summer squash": ["zucchini"],
            "crookneck squash": ["squash"],
            "gem squash": ["squash"],
            "pattypan squash": ["squash"],
            "straightneck squash": ["squash"],
            "zucchinis": ["zucchini"],
            "kamokamo": ["squash"],
            "aehobak": ["zucchini"],
            "tromboncino": ["squash"],
            "zucchetta": ["squash"],
            "squashes": ["squash"],
            "melons": ["melon"],
            "watermelon": ["water melon"],
            "watermelons": ["watermelon", "water melon"],
            "water melon": ["watermelon"],
            "water melons": ["watermelon","water melon"],
            "true melon": ["sweet melons"],
            "horned melon": ["sweet melons"],
            "table beets": ["beets table"],
            "table beet": ["beets table"],
            "beetroot": ["beets table"],
            "garden beets": ["beets table"],
            "garden beet": ["beets table"],
            "dinner beets": ["beets table"],
            "dinner beet": ["beets table"],
            "parsnips": ["parsnip"],
            "potatoes": ["potato"],
            "spud": ["potato"],
            "sweet potatoes": ["sweet potato"],
            "turnips": ["turnip"],
            "rutabagas": ["rutabaga"],
            "swedish turnip": ["turnip"],
            "white turnip": ["turnip"],
            "sugarbeet": ["sugar beet"],
            "sugar beets": ["sugar beet","sugarbeet"],
            "sugarbeets": ["sugar beet","sugarbeet"],
            "green beans": ["beans green"],
            "greenbeans": ["beans green"],
            "green bean": ["beans green"],
            "greenbean": ["beans green"],
            "bean": ["chickpea","garbanzo"],
            "beans": ["bean","chickpea","garbanzo"],
            "dry beans": ["beans dry"],
            "dry broad beans": ["beans dry"],
            "pulses": ["beans dry"],
            "chick pea": ["chickpea"],
            "chickpeas": ["chickpea"],
            "chick peas": ["chickpea"],
            "fababean": ["faba bean"],
            "garbanzo bean": ["garbanzo"],
            "garbanzo beans": ["garbanzo"],
            "peanuts": ["peanut"],
            "groundnuts": ["groundnut"],
            "goober": ["peanut"],
            "goober pea": ["peanut"],
            "goober peas": ["peanut"],
            "pindar": ["peanut"],
            "monkey nut": ["peanut"],
            "lentils": ["lentil"],
            "black-eyed pea": ["cowpea"],
            "black-eyed peas": ["cowpea"],
            "soy bean": ["soybeans"],
            "soy beans": ["soybeans"],
            "soya bean": ["soybeans"],
            "artichokes": ["artichoke"],
            "french artichoke": ["artichoke"],
            "globe artichoke": ["artichoke"],
            "green artichoke": ["artichoke"],
            "mentha": ["mint"],
            "strawberry": ["strawberries"],
            "garden strawberry": ["strawberries"],
            "upland cotton": ["cotton"],
            "extra-long staple cotton": ["cotton"],
            "tree cotton": ["cotton"],
            "levant cotton": ["cotton"],
            "pima cotton": ["cotton"],
            "common flax": ["flax"],
            "linseed": ["flax"],
            "castorbean": ["castor bean"],
            "castor bean": ["castorbean"],
            "castorbeans": ["castorbean", "castor bean"],
            "castor beans": ["castorbean", "castor bean"],
            "ricinus": ["castorbean", "castor bean"],
            "castor oil plant": ["castorbean", "castor bean"],
            "rape": ["rapeseed"],
            "oilseed rape": ["rapeseed"],
            "simsim": ["sesame"],
            "benne": ["sesame"],
            "gingelly": ["sesame"],
            "sunflowers": ["sunflower"],
            "common sunflowers": ["sunflower"],
            "common sunflower": ["sunflower"],
            "common oat": ["oats"],
            "common oats": ["oats"],
            "corn": ["maize"],
            "zea mays": ["maize"],
            "field corn": ["maize field", "maize grain"],
            "sweet corn": ["maize sweet"],
            "millets": ["millet"],
            "finger millet": ["millet"],
            "pearl millet": ["millet"],
            "little millet": ["millet"],
            "sorghum": ["sorghum"],
            "great millet": ["sorghum"],
            "broomcorn": ["sorghum"],
            "guinea corn": ["sorghum"],
            "durra": ["sorghum"],
            "imphee": ["sorghum"],
            "jowar": ["sorghum"],
            "milo": ["sorghum"],
            "indica rice": ["rice"],
            "japonica rice": ["rice"],
            "lucerne": ["alfalfa"],
            "bermudagrass": ["bermuda"],
            "bermuda grass": ["bermuda"],
            "coastal bermudagrass": ["bermuda"],
            "berseem clover": ["clover"],
            "egyptian clover": ["clover"],
            "ryegrass": ["rye grass"],
            "sudan grass": ["sudan"],
            "sudan grass hay": ["sudan"],
            "turf grass": ["turfgrass"],
            "lawn grass": ["turfgrass"],
            "bananas": ["banana"],
            "cacao tree": ["cacao"],
            "cocoa tree": ["cacao"],
            "cocoa": ["cacao"],
            "arabica coffee": ["coffee"],
            "coffea arabica": ["coffee"],
            "coffee plant": ["coffee"],
            "dates": ["date palms"],
            "palms": ["palm trees"],
            "pineapples": ["pineapple"],
            "ananas": ["pineapple"],
            "rubber plant": ["rubber trees"],
            "sharinga tree": ["rubber trees"],
            "para rubber tree": ["rubber trees"],
            "rubber plants": ["rubber trees"],
            "tea tree": ["tea"],
            "tea plant": ["tea"],
            "tea shrub": ["tea"],
            "tea trees": ["tea"],
            "tea plants": ["tea"],
            "tea shrubs": ["tea"],
            "berry": ["berries", "strawberries"],
            "berry shrub": ["berries bushes"],
            "berry bushes": ["berries bushes"],
            "berry bush": ["berries bushes"],
            "blueberries": ["berries bushes"],
            "blueberry": ["berries bushes"],
            "boysenberry": ["berries bushes"],
            "elderberry": ["berries bushes"],
            "blackberry": ["berries bushes"],
            "blackberries": ["berries bushes"],
            "raspberry": ["berries bushes"],
            "raspberries": ["berries bushes"],
            "wine grape": ["grapes wine"],
            "wine grapes": ["grapes wine"],
            "table grape": ["grapes table"],
            "table grapes": ["grapes table"],
            "raisin": ["grapes table"],
            "hops plant": ["hops"],
            "almond tree": ["almonds"],
            "almond trees": ["almonds"],
            "apple tree": ["apples"],
            "apple trees": ["apples"],
            "apple": ["apples"],
            "cherry": ["cherries"],
            "cherry tree": ["cherries"],
            "cherry trees": ["cherries"],
            "pear tree": ["pears"],
            "pear trees": ["pears"],
            "apricot tree": ["apricots"],
            "apricot trees": ["apricots"],
            "peach tree": ["peaches"],
            "peach trees": ["peaches"],
            "stone fruits": ["stone fruit"],
            "avocados": ["avocado"],
            "citrus trees": ["citrus"],
            "citrus tree": ["citrus"],
            "oranges": ["citrus"],
            "orange": ["citrus"],
            "orange tree": ["citrus"],
            "orange trees": ["citrus"],
            "grapefruits": ["citrus"],
            "grapefruit": ["citrus"],
            "grapefruit trees": ["citrus"],
            "grapefruit tree": ["citrus"],
            "limes": ["citrus"],
            "lime": ["citrus"],
            "lime tree": ["citrus"],
            "lime trees": ["citrus"],
            "lemon": ["citrus"],
            "lemons": ["citrus"],
            "lemon tree": ["citrus"],
            "lemon trees": ["citrus"],
            "tangerine": ["citrus"],
            "tangerines": ["citrus"],
            "tangerine trees": ["citrus"],
            "tangerine tree": ["citrus"],
            "conifer tree": ["conifer trees"],
            "coniferous trees": ["conifer trees"],
            "coniferous tree": ["conifer trees"],
            "spruce trees": ["conifer trees"],
            "spruce tree": ["conifer trees"],
            "pine trees": ["conifer trees"],
            "pine tree": ["conifer trees"],
            "fir trees": ["conifer trees"],
            "fir tree": ["conifer trees"],
            "kiwis": ["kiwi"],
            "kiwifruit": ["kiwi"],
            "chinese gooseberry": ["kiwi"],
            "chinese gooseberries": ["kiwi"],
            "kiwifruits": ["kiwi"],
            "green olive": ["olives"],
            "black olive": ["olives"],
            "green olives": ["olives"],
            "black olives": ["olives"],
            "olive tree": ["olives"],
            "olive trees": ["olives"],
            "pistachio tree": ["pistachios"],
            "pistachio trees": ["pistachios"],
            "walnuts": ["walnut"],
            "walnut tree": ["walnut"],
            "walnut trees": ["walnut"],
            "january": ["jan"],
            "february": ["feb"],
            "march": ["mar"],
            "april": ["apr"],
            "june": ["jun"],
            "july": ["jul"],
            "august": ["aug"],
            "september": ["sep"],
            "october": ["oct"],
            "november": ["nov"],
            "december": ["dec"]
        }

    def search11(self,phrase,usesyn=True):
        """Search FAO-56 Table 11 based on the provided phrase

        Parameters
        ----------
        phrase : str
            String expression for searching FAO-56 Table 11
        usesyn : boolean, optional
            Whether or not to use the synonym dictionary (default=True)

        Returns
        -------
        table11sub : DataFrame
            Subsetted FAO-56 Table 11 based on the search phrase
        """

        phrase = phrase.lower()
        phrases = [phrase]
        if usesyn and phrase in self.synonyms.keys():
            phrases += self.synonyms[phrase]
        indices = list()
        df = self.table11
        for col in ['Crop','Plant Date','Region']:
            for phrase in phrases:
                temp =  df[df[col].str.contains(phrase)].index.values
                indices += temp.tolist()
        table11sub = self.table11.iloc[list(set(indices))]
        return table11sub

    def search12(self,phrase,usesyn=True):
        """Search FAO-56 Table 12 based on the provided phrase

        Parameters
        ----------
        phrase : str
            String expression for searching FAO-56 Table 12
        usesyn : boolean, optional
            Whether or not to use the synonym dictionary (default=True)

        Returns
        -------
        table12sub : DataFrame
            Subsetted FAO-56 Table 12 based on the search phrase
        """

        phrase = phrase.lower()
        phrases = [phrase]
        if usesyn and phrase in self.synonyms.keys():
            phrases += self.synonyms[phrase]
        indices = list()
        df = self.table12
        for phrase in phrases:
            temp = df[df['Crop'].str.contains(phrase)].index.values
            indices += temp.tolist()
        table12sub = self.table12.iloc[list(set(indices))]
        return table12sub

    def search17(self,phrase,usesyn=True):
        """Search FAO-56 Table 17 based on the provided phrase

        Parameters
        ----------
        phrase : str
            String expression for searching FAO-56 Table 17
        usesyn : boolean, optional
            Whether or not to use the synonym dictionary (default=True)

        Returns
        -------
        table17sub : DataFrame
            Subsetted FAO-56 Table 17 based on the search phrase
        """

        phrase = phrase.lower()
        phrases = [phrase]
        if usesyn and phrase in self.synonyms.keys():
            phrases += self.synonyms[phrase]
        indices = list()
        df = self.table17
        for phrase in phrases:
            temp = df[df['Crop'].str.contains(phrase)].index.values
            indices += temp.tolist()
        table17sub = self.table17.iloc[list(set(indices))]
        return table17sub

    def search22(self,phrase,usesyn=True):
        """Search FAO-56 Table 22 based on the provided phrase

        Parameters
        ----------
        phrase : str
            String expression for searching FAO-56 Table 22
        usesyn : boolean, optional
            Whether or not to use the synonym dictionary (default=True)

        Returns
        -------
        table17sub : DataFrame
            Subsetted FAO-56 Table 22 based on the search phrase
        """

        phrase = phrase.lower()
        phrases = [phrase]
        if usesyn and phrase in self.synonyms.keys():
            phrases += self.synonyms[phrase]
        indices = list()
        df = self.table22
        for phrase in phrases:
            temp = df[df['Crop'].str.contains(phrase)].index.values
            indices += temp.tolist()
        table22sub = self.table22.iloc[list(set(indices))]
        return table22sub
