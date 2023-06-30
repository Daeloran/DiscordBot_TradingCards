# cards.py

class Card:
    def __init__(self, card_number, name, rarity, image_url):
        self.card_number = card_number
        self.name = name
        self.rarity = rarity
        self.image_url = image_url


    def to_dict(self):
        return {
            "card_number": self.card_number,
            "name": self.name,
            "rarity": self.rarity,
            "image_url": self.image_url
        }
    
    def lower(self):
        return str(self).lower()

    def __str__(self):
        return self.name

class User:
    def __init__(self, username):
        self.username = username
        self.searches = []  # Liste des recherches en cours de l'utilisateur (contenant des objets Card)
        self.trades = []  # Liste des échanges en cours de l'utilisateur (contenant des objets Card)
        self.score = 0  # Score de l'utilisateur
    
    def reset(self):
        self.searches = []
        self.trades = []
        self.score = 0
    
    def to_dict(self):
        return {
            "username": self.username,
            "searches": [card.to_dict() for card in self.searches],
            "trades": [card.to_dict() for card in self.trades],
            "score": self.score,
        }
    
    @classmethod
    def from_dict(cls, data):
        user = cls(data['username'])
        user.searches = [Card(card_info['card_number'], card_info['name'], card_info['rarity'], card_info['image_url']) for card_info in data['searches']]
        user.trades = [Card(card_info['card_number'], card_info['name'], card_info['rarity'], card_info['image_url']) for card_info in data['trades']]
        user.score = data['score']
        return user


available_cards = [
    Card("1", "NAVIRE PIRATE", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_001_f52bd649-722f-456b-902c-ebad06087963.jpg?v=1687425530"),
    Card("2", "PORTAL", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_002_572e1a8a-028c-460f-bee3-f1d19ae45fa9.jpg?v=1687425530"),
    Card("3", "QUANTUM", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_003_b77985d2-2529-4555-a9ac-70ed87437367.jpg?v=1687425530"),
    Card("4", "ROCKET FIELD", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_004_03588a17-7b68-4727-94de-1008453b1bd0.jpg?v=1687425531"),
    Card("5", "RUST", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_005_f61473cf-8ae0-41ec-86b2-8585e7458235.jpg?v=1687425531"),
    Card("6", "IL FAIT PAS CHAUD", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_006_d7b1ab5b-13dc-41dd-b4bc-b1202e8f4ce4.jpg?v=1687425531"),
    Card("7", "GOLF", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_007_cf833b53-2587-4b34-8773-75e6cf82c2de.jpg?v=1687425530"),
    Card("8", "DUST 2", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_008_06cc78a9-dabe-414a-b0e3-d047ddaca889.jpg?v=1687425530"),
    Card("9", "SPACE FACTORY", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_009_08fb3d58-bfeb-411d-ac39-6ca84d07eeff.jpg?v=1687425530"),
    Card("10", "LA F.A.Q", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_010_7faa767a-6748-439a-9b66-74af806596d9.jpg?v=1687425530"),
    Card("11", "MUSEE", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_011_26fdac61-3b6f-40ef-91c9-8f5dfab00eb9.jpg?v=1687425530"),
    Card("12", "FNAF", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_012_58cd69b1-89da-49c0-acd4-f360e4875e1d.jpg?v=1687425530"),
    Card("13", "VILLAGE", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_013_2ef0c31d-4ab6-4d22-b2bb-6ab34b227f28.jpg?v=1687425530"),
    Card("14", "LA FERME", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_014_aeb2b900-a402-49eb-8062-515f6ce1d47b.jpg?v=1687425529"),
    Card("15", "SOCISSEAU FACTORY", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_015_fb69637a-fb25-4791-a558-50d91e790822.jpg?v=1687425530"),
    Card("16", "TROU DU MONDE", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_016_cf1cfdff-d44c-4e27-bf17-4c55ffdf198d.jpg?v=1687425530"),
    Card("17", "MORIA", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_017_8d37f4f8-dfa7-47ac-a690-e2517133c0f1.jpg?v=1687425531"),
    Card("18", "TCHERNOBYL", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_018_4efff718-faff-4bb8-bac2-660da41cdb07.jpg?v=1687425530"),
    Card("19", "VALHEIM", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_019_da33b4d8-df4e-4c86-acb4-c7862143ac23.jpg?v=1687425530"),
    Card("20", "TRANCHEES", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_020_6812aaa6-57f7-4022-8e38-27b22defe0de.jpg?v=1687425531"),
    Card("21", "RAVENHOLM", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_021_aac2ff6b-9a9c-4e5f-ba0b-73e89c9b2a42.jpg?v=1687425560"),
    Card("22", "URBEX", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_022_f03674cf-47e2-4c5b-a87b-45ac5e7e93a3.jpg?v=1687425556"),
    Card("23", "MANOIR", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_023_7562e90a-8f0f-4782-b215-c03269995006.jpg?v=1687425558"),
    Card("24", "BARRAGE", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_024_9659fa25-2dec-4801-bd53-8697d7c3ecf5.jpg?v=1687425558"),
    Card("25", "CHERNOGORSK", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_025_20bac7c6-97a9-4a49-9b3f-dc834de55935.jpg?v=1687425556"),
    Card("26", "AGROU", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_026_56d1310c-8479-4394-9d21-75b580d03c70.jpg?v=1687425559"),
    Card("27", "GARAGE", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_027_cb8e9d75-2cc0-4932-a54d-27462ed9f8d1.jpg?v=1687425558"),
    Card("28", "URETUS", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_028_9f1b8685-4e1a-4cb0-abfd-839b712ec815.jpg?v=1687425558"),
    Card("29", "WANKIL SHOW", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_029_a1d74e4a-b712-4320-ba80-664f22f4c46d.jpg?v=1687425558"),
    Card("30", "CONVENTION", "Terrain", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_030_c065c38d-a0ac-4041-9923-483b6ade1e81.jpg?v=1687425558"),
    Card("31", "GARAGISTE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_031_18c217f2-72c2-4506-86a6-58a4edb5f0bc.jpg?v=1687425558"),
    Card("32", "GARAGISTE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_032_91c9f67a-79e7-4e50-b378-862894885209.jpg?v=1687425556"),
    Card("33", "CAMIONNEUR", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_033_5875f515-be96-4f26-bdc0-77425882f723.jpg?v=1687425557"),
    Card("34", "CAMIONNEUR", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_034_4e494a06-621a-4174-a61d-67946cdc1229.jpg?v=1687425557"),
    Card("35", "VENDEUR", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_035_1a1c8b42-8f30-45c7-bf55-a70da3299140.jpg?v=1687425558"),
    Card("36", "VENDEUR", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_036_47bac568-7789-431b-8cbd-a1c76ef399ce.jpg?v=1687425558"),
    Card("37", "ANNABELLE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_037_bb8bee58-5ded-4266-b1a2-39be02744f0d.jpg?v=1687425559"),
    Card("38", "GRUDGE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_038_901ddf4c-3025-4fb3-9ca0-bd090a195819.jpg?v=1687425557"),
    Card("39", "ASTRONAUTE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_039_df912090-e933-4254-a86d-dd9432a49816.jpg?v=1687425558"),
    Card("40", "ASTRONAUTE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_040_1943cd7c-31fe-41b8-934b-a4683b479588.jpg?v=1687425558"),
    Card("41", "BOXEUR", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_041_aeaf307c-cd06-4d25-9d8e-132e0e6da2d1.jpg?v=1687425558"),
    Card("42", "BOXEUR", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_042_47bc6b3b-2c7f-4545-9576-0dec559b78a4.jpg?v=1687425557"),
    Card("43", "INFECTÉ", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_043_518faff8-2cc1-4832-94f1-d1da0261b370.jpg?v=1687425557"),
    Card("44", "INFECTÉ", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_044_ca758076-8116-4606-a9ca-6b37d2c7c7c0.jpg?v=1687425556"),
    Card("45", "FERMIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_045_27ea4703-f2e0-4bd8-b3fc-3e541edc4025.jpg?v=1687425557"),
    Card("46", "FERMIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_046_f2b85d41-07a7-4b8d-a8be-5968b71086b4.jpg?v=1687425557"),
    Card("47", "CHIEN", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_047_490754dd-243f-4ff6-b2fb-c669b1be5bd4.jpg?v=1687425556"),
    Card("48", "COCHON", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_048_cd354dc5-33ef-4c4b-ae0d-f016a550d8c2.jpg?v=1687425556"),
    Card("49", "FROMAGER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_049_24c906cf-54bc-4e68-8a41-9693d29a6f33.jpg?v=1687425556"),
    Card("50", "CHARCUTIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_050_47918c8c-9507-44ec-9f88-9e054fec20d4.jpg?v=1687425557"),
    Card("51", "BUSINESSMAN", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_051_8739d087-dc26-46e2-986f-042e88aad3cc.jpg?v=1687425557"),
    Card("52", "DÉBILE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_052_d6db2ec4-c970-4f96-95b7-a96a798f5a83.jpg?v=1687425558"),
    Card("53", "DÉBILE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_053_5c060805-53fa-4f2f-80d5-6baa9ca1e709.jpg?v=1687425559"),
    Card("54", "PAYSAN", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_054_3c396196-7f56-43e4-8d0a-0479c132c365.jpg?v=1687425558"),
    Card("55", "PAYSAN", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_055_e6d21e75-8dcb-423b-9f45-34f42d4d6f4d.jpg?v=1687425559"),
    Card("56", "CUISINIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_056_8edc0298-89a0-4886-85d9-c89e8f633eeb.jpg?v=1687425558"),
    Card("57", "CUISINIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_057_e8c0b154-6072-4fc5-9f5b-861c06f1048f.jpg?v=1687425558"),
    Card("58", "BÉBÉ", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_058_c069bf49-5008-4ce5-89f1-0c9e042d4b13.jpg?v=1687425558"),
    Card("59", "BÉBÉ", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_059_66f749c7-10e8-4799-b6b3-40286a5ed782.jpg?v=1687425559"),
    Card("60", "CHASSEUR", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_060_63d6397a-e758-440c-b02f-6512acd81fcb.jpg?v=1687425558"),
    Card("61", "PILOTE D'AVION", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_061_3ecb14c0-76e8-447a-8a76-8c8ab17e7ac6.jpg?v=1687425558"),
    Card("62", "AGROU", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_062_42a1d6d8-6622-477a-b466-d254af63a213.jpg?v=1687425558"),
    Card("63", "AGROU", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_063_5336ee6c-76fe-47dd-83dd-caf441d7934b.jpg?v=1687425556"),
    Card("64", "CHEVALIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_064_294a8ac8-df08-403b-9bce-681b8f20b321.jpg?v=1687425558"),
    Card("65", "CHEVALIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_065_a8dedcef-fcb8-4e8b-a087-e5107a5346a1.jpg?v=1687425558"),
    Card("66", "PEINTRE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_066_e81ad750-38d8-4038-9c92-c62c86610a70.jpg?v=1687425558"),
    Card("67", "PEINTRE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_067_4960fc56-f8c4-44ee-9e9f-042088fecd7c.jpg?v=1687425558"),
    Card("68", "POMPIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_068_45aa6a2b-e7a5-4149-a9bd-b1c15a9ac207.jpg?v=1687425558"),
    Card("69", "POMPIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_069_22d7c075-3c81-4f4d-b6a2-5defac63a56b.jpg?v=1687425559"),
    Card("70", "SORCIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_070_e37b9a3f-7847-4b79-85dd-5852ffc5dc48.jpg?v=1687425558"),
    Card("71", "SORCIER", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_071_0377731e-7863-4f80-8d69-a311f42ac13f.jpg?v=1687425558"),
    Card("72", "SDF", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_072_db2d8a47-33d3-4ca8-a046-f32dada9af8b.jpg?v=1687425558"),
    Card("73", "SDF", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_073_685c6094-a7b7-441a-bbb4-49984c2a7969.jpg?v=1687425558"),
    Card("74", "TOURISTE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_074_516c38c7-f80b-4c30-9d63-d3d27b7a73ae.jpg?v=1687425559"),
    Card("75", "TOURISTE", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_075_ad2683da-73bb-4c96-a76c-12c64eb7e3d3.jpg?v=1687425558"),
    Card("76", "EMPLOYÉ WCDO", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_076_67ee1909-87d3-453d-b1fe-db48af545abf.jpg?v=1687425558"),
    Card("77", "EMPLOYÉ WCDO", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_077_ec2ed007-910d-47f3-bfce-df073630e428.jpg?v=1687425558"),
    Card("78", "MORT-VIVANT", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_078_1d9ce266-fb2e-4183-be64-b73355b8f0af.jpg?v=1687425556"),
    Card("79", "MORT-VIVANT", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_079_bb4d57b6-3581-47ba-84a5-7087fdcb5493.jpg?v=1687425557"),
    Card("80", "SOLDAT ROMAIN", "Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_080_7ac6c1e5-9350-48a2-b027-e0ca5d4264d8.jpg?v=1687425558"),
    Card("81", "SPIDERLAINK", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_081_9eb1d706-5a02-47b0-a099-c9ae42e814a5.jpg?v=1687425559"),
    Card("82", "THORRACID", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_082_dff0fba9-03b4-4e98-943f-6462be960866.jpg?v=1687425558"),
    Card("83", "CT", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_083_3be3e0d0-5b03-48b2-9b12-5ebf7f9a4d05.jpg?v=1687425557"),
    Card("84", "TERRO", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_084_fa4aede2-b63a-4178-9ca0-b2ddee0f9cb3.jpg?v=1687425557"),
    Card("85", "CLOWN TUEUR", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_085_926c74c8-b149-428a-ab6a-baceb13e290c.jpg?v=1687425557"),
    Card("86", "JOUEUR DU GRENIER", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_086_bebff767-f2de-4ef6-b2c8-1a33b2adc382.jpg?v=1687425559"),
    Card("87", "SEB", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_087_4d0f9ebf-35ea-4eed-8999-f5070b54660f.jpg?v=1687425559"),
    Card("88", "AMIXEM", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_088_e8aec808-4a43-4be4-bd86-feb28fb07230.jpg?v=1687425557"),
    Card("89", "PIRATE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_089_0a7df109-ad96-405f-aa64-4c2d7df9bc47.jpg?v=1687425559"),
    Card("90", "PIRATE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_090_33a55020-d105-4d46-a63f-8b97bcc34059.jpg?v=1687425558"),
    Card("91", "SEMI-HOMME", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_091_bb3d2b4d-bd98-4f61-aff5-0b68223d3350.jpg?v=1687425559"),
    Card("92", "SEMI-HOMME", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_092_e6880d3c-e9e0-4e4e-9965-67439155dbe8.jpg?v=1687425558"),
    Card("93", "MARTHIE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_093_6c104454-9970-4230-a4a2-f8c382b5b793.jpg?v=1687425558"),
    Card("94", "DOC", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_094_aa9b8c41-c02d-4d95-a921-b73e7174febf.jpg?v=1687425559"),
    Card("95", "VIEILLE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_095_51d400ac-2ef7-4d87-baf2-c08a1873a5f5.jpg?v=1687425559"),
    Card("96", "VIEILLE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_096_e9f7822b-ff7c-4a79-aaae-c0ff98408449.jpg?v=1687425559"),
    Card("97", "FANBOY", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_097_fb115b27-6648-4a8e-be2c-16e710d56720.jpg?v=1687425557"),
    Card("98", "FANGIRL", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_098_36e089fa-538b-4a36-9bd9-194d3a0a89b0.jpg?v=1687425557"),
    Card("99", "GOTAGA", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_099_3865b1ba-e370-40ca-919e-47641fc5b044.jpg?v=1687425558"),
    Card("100", "BILLY BONHOMME DE NEIGE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_100_13c451f2-d223-42fa-820c-427c6462a657.jpg?v=1687425558"),
    Card("101", "GREMLIN", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_101_794ff496-cea0-44bf-b780-f7f88b24ec18.jpg?v=1687425557"),
    Card("102", "STEVE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_102_5f6a2db8-f394-40b7-aafe-7ed796445994.jpg?v=1687425557"),
    Card("103", "STEVE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_103_7a6aefd2-6aa8-4207-84b7-a2b2fd7ed6d1.jpg?v=1687425558"),
    Card("104", "APPRENTIE SORCIÈRE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_104_9cc73c16-1903-4cf9-a946-dea4f374d165.jpg?v=1687425556"),
    Card("105", "ELFE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_105_02170b9f-8130-447c-a2a0-ff0088f1adec.jpg?v=1687425557"),
    Card("106", "SEL", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_106_7db3098a-b162-4e1e-a0ae-46ab5fc1eabe.jpg?v=1687425556"),
    Card("107", "SEL", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_107_30ae3f0d-edeb-4cde-8ac6-31e0dc271598.jpg?v=1687425556"),
    Card("108", "MASTU", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_108_e39c22da-a1a6-4b1b-898f-dfa4acc5de83.jpg?v=1687425558"),
    Card("109", "DEOTOONS", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_109_d52b54dc-1d7d-4494-a641-7e81da2c2208.jpg?v=1687425558"),
    Card("110", "COWBOY", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_110_d2ce6d76-6440-45c5-8a65-5a07ac89dc85.jpg?v=1687425558"),
    Card("111", "COWBOY", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_111_0b9f942f-cefa-4539-a468-319576ecc73f.jpg?v=1687425559"),
    Card("112", "POLICIER", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_112_31c427fc-0f9b-40e9-b9ef-7f72b3e5d3a2.jpg?v=1687425558"),
    Card("113", "POLICIER", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_113_a565c8be-0176-487f-ab96-1951a8c1f4fa.jpg?v=1687425557"),
    Card("114", "OBÈSE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_114_4487f0c5-7407-4da6-bdba-a10b83dad8f4.jpg?v=1687425558"),
    Card("115", "SINGE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_115_b2936fc7-b516-4b56-892b-59047dda244b.jpg?v=1687425558"),
    Card("116", "ENQUÊTEUR", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_116_4ad4a144-9681-4214-9797-6b15bd551a4d.jpg?v=1687425559"),
    Card("117", "POTATOZ", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_117_6fdfbb9d-621d-4e74-8abd-5191015b9a9c.jpg?v=1687425558"),
    Card("118", "JIRAYA", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_118_8d2f3609-f68a-4716-b53f-cfd83ec4c056.jpg?v=1687425559"),
    Card("119", "FELDUP", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_119_fd842e88-0125-42a9-af0d-ffcd121c4909.jpg?v=1687425559"),
    Card("120", "BRETONNE BIGOUDENE", "Peu Commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_120_d89afac6-c923-4f90-a23e-f07a32b14e79.jpg?v=1687425559"),
    Card("121", "ROI", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_121_66d86f72-7db0-4da4-9275-fe9135559f90.jpg?v=1687425559"),
    Card("122", "HUGO DÉLIRE", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_122_718dbe25-ad17-4eef-b1d3-ceff991d88f2.jpg?v=1687425559"),
    Card("123", "XARI", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_123_dca7843f-a02d-4b54-91ca-58adb531bdd3.jpg?v=1687425559"),
    Card("124", "PRINCESSE", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_124_2cd10cda-ccf8-4f3f-a39c-f909054d5236.jpg?v=1687425560"),
    Card("125", "PRINCESSE", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_125_5e23879f-435f-4f8e-a04d-44583dbc5b1c.jpg?v=1687425560"),
    Card("126", "PROSTITUÉE", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_126_bf27326b-8c0d-49b3-8e83-7967a859019b.jpg?v=1687425559"),
    Card("127", "FÉE", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_127_c4298423-8174-4fca-b305-76a6ccde1b59.jpg?v=1687425560"),
    Card("128", "G CRAMÉ", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_128_661cd82f-6cf4-4df3-8bdd-f4b99b2f7bb9.jpg?v=1687425559"),
    Card("129", "SUPERCONERI", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_129_e109d99a-0df8-4c6a-8d3a-9c8dd21615d6.jpg?v=1687425559"),
    Card("130", "MOINE", "Peu commune", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_130_35034a2d-0f3a-45f5-b9bf-90dedc42eb65.jpg?v=1687425559"),
    Card("131", "CYBERLAINK", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_131_ec787eee-5d82-46bc-87b0-8a9e1fefa74b.jpg?v=1687425582"),
    Card("132", "CYBERTERRA", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_132_da341896-b017-401d-9b3d-f9638b71fe70.jpg?v=1687425582"),
    Card("133", "JACQUES FLANTIER", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_133_52e541f5-d8ac-48aa-a124-d96a246e96d3.jpg?v=1687425581"),
    Card("134", "RICHARD FLANTIER", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_134_630daaa4-9135-4e2d-91a0-038b767a2a30.jpg?v=1687425581"),
    Card("135", "DRESSEUR", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_135_668c4d6e-5b02-4f5e-915f-30f87b352e37.jpg?v=1687425581"),
    Card("136", "DRESSEUSE", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_136_3ac6f1e8-8817-4365-8eaa-d2e244186d76.jpg?v=1687425582"),
    Card("137", "SURVIVANT", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_137_1e8e617d-e0dc-4027-92ac-210f8ba7fbe9.jpg?v=1687425582"),
    Card("138", "SURVIVANT", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_138_e72c24a7-c93a-4f69-ae47-00be2edcfa28.jpg?v=1687425582"),
    Card("139", "WICROMANIA", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_139_9af4754d-46b1-4fb5-8821-0d44a6ffe366.jpg?v=1687425582"),
    Card("140", "VOYANT", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_140_276660ee-9f71-42b3-a9df-f25e99ce9963.jpg?v=1687425582"),
    Card("141", "PIERRE RONDIN", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_141_9df56696-36cd-40e1-a40a-78ea1aca690a.jpg?v=1687425581"),
    Card("142", "ANDRÉ RONDIN", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_142_333ac136-de47-4501-8330-1d9acc21f7b7.jpg?v=1687425581"),
    Card("143", "PROFESSEUR", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_143_bc306d93-af2d-4032-b2a1-edd7e3aba902.jpg?v=1687425582"),
    Card("144", "PROFESSEUR", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_144_7aa04c91-b06f-4b1e-85eb-1995b5909caf.jpg?v=1687425582"),
    Card("145", "SAMOURAÏ", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_145_35bcae9c-1848-4eeb-bfce-1ca61b7cf317.jpg?v=1687425582"),
    Card("146", "SAGE JAPONAIS", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_146_27ee5b6a-ff24-4fd6-afb5-d1b9cb59726c.jpg?v=1687425582"),
    Card("147", "JEANINE", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_147_3664c877-d3b1-4ff9-a0d2-a641feb4cd6b.jpg?v=1687425582"),
    Card("148", "MARTINE", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_148_808e052f-800d-4057-8480-60080628c52a.jpg?v=1687425583"),
    Card("149", "LAINK", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_149_7a11a624-cce3-42cb-9832-a0ca9fa6dd57.jpg?v=1687425582"),
    Card("150", "TERRACID", "Rare", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_150_2999ec48-b219-4b88-94f3-afa8da6b4f76.jpg?v=1687425581"),
    Card("151", "COWBOY", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_151_7944a96b-e9a9-44ed-9883-6947569c2fb6.jpg?v=1687425582"),
    Card("152", "COWBOY", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_152_11cc0f53-eb51-4f5c-9bdf-f3bebb33b435.jpg?v=1687425582"),
    Card("153", "POLICIER", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_153_eeb88211-82ab-4a20-a6de-7e51dd8c1f80.jpg?v=1687425582"),
    Card("154", "POLICIER", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_154_cc4558a5-d555-4f69-b8f8-801dc7684a65.jpg?v=1687425582"),
    Card("155", "SEL", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_155_5647fc53-86b8-487e-b4b5-c43f98e17337.jpg?v=1687425582"),
    Card("156", "SEL", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_156_a6ae8ddc-afc1-4b7f-abf3-b3b1d28ca130.jpg?v=1687425581"),
    Card("157", "FROMAGER", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_157_ee5a2522-3ebd-4fe2-bbb5-ab083fb44456.jpg?v=1687425581"),
    Card("158", "CHARCUTIER", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_158_eeb05872-9ac8-40c2-bac8-10b8b63be7c4.jpg?v=1687425582"),
    Card("159", "GOTAGA", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_159_271c4198-a141-4985-a856-dfe2df90440d.jpg?v=1687425582"),
    Card("160", "AMIXEM", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_160_e38ef95f-e540-408d-8787-cd6173ca6d84.jpg?v=1687425582"),
    Card("161", "PIRATE", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_161_ab46c840-e509-452a-af29-986d0838161b.jpg?v=1687425582"),
    Card("162", "PIRATE", "Ultra rare holo 1", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_162_9d627e1b-2eb3-4b06-aa65-48275814cebc.jpg?v=1687425582"),
    Card("163", "MASTU", "Ultra rare holo 2", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_163_8bd54bcd-a322-402a-a179-9d4d47b49971.jpg?v=1687425581"),
    Card("164", "G CRAMÉ", "Ultra rare holo 2", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_164_6eed4209-4523-4b3b-a446-608907e35e61.jpg?v=1687425581"),
    Card("165", "CT", "Ultra rare holo 2", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_165_f2e4bfe5-a50d-43a8-80f4-09d742c6e894.jpg?v=1687425581"),
    Card("166", "TERRO", "Ultra rare holo 2", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_166_ca4446f7-5a34-484c-88d6-44e1f092ab94.jpg?v=1687425581"),
    Card("167", "JOUEUR DU GRENIER", "Ultra rare holo 2", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_167_5f579c7b-dee5-48f7-808b-f8ae5085b647.jpg?v=1687425581"),
    Card("168", "SEB", "Ultra rare holo 2", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_168_d3ff9efa-b6e4-47eb-bba2-77e922a4fae8.jpg?v=1687425582"),
    Card("169", "WICROMANIA", "Légendaire Bronze", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_169_e19a1dfa-77f4-4f69-bb39-e3e90539fbea.jpg?v=1687425582"),
    Card("170", "VOYANT", "Légendaire Bronze", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_170_3b3a516a-4f60-4a19-a160-569601b9a195.jpg?v=1687425582"),
    Card("171", "PIERRE RONDIN", "Légendaire Bronze", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_171_3d11b069-8b07-4d30-823e-0c25a2b8e3e6.jpg?v=1687425581"),
    Card("172", "ANDRÉ RONDIN", "Légendaire Bronze", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_172_3244b979-9fd3-4936-a01a-4e10301ace0e.jpg?v=1687425582"),
    Card("173", "SURVIVANT", "Légendaire Bronze", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_173_1fa45820-7aa3-4995-80fa-86572cfca820.jpg?v=1687425582"),
    Card("174", "SURVIVANT", "Légendaire Bronze", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_174_4e71182a-8af9-458b-8f11-9c758db74b00.jpg?v=1687425582"),
    Card("175", "JACQUES FLANTIER", "Légendaire Argent", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_175_55c9da07-61c5-4191-b3e0-fef8cf103d52.jpg?v=1687425582"),
    Card("176", "RICHARD FLANTIER", "Légendaire Argent", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_176_b040084c-55d8-42bc-9508-31bc296ed041.jpg?v=1687425581"),
    Card("177", "JEANINE", "Légendaire Argent", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_177_27dd98aa-9ebb-4751-b082-789dc82468fe.jpg?v=1687425582"),
    Card("178", "MARTINE", "Légendaire Argent", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_178_909c9ed3-5186-46cb-840b-316d3c906f19.jpg?v=1687425582"),
    Card("179", "LAINK", "Légendaire Or", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_179_b0b90c77-7eb0-4394-8f01-91f431a8e9eb.jpg?v=1687425582"),
    Card("180", "TERRACID", "Légendaire Or", "https://cdn.shopify.com/s/files/1/0683/2055/9412/files/Wankul_180_0f1f186a-a374-40e8-a8b3-01a4bfbae2ae.jpg?v=1687425582"),
    # Ajoute d'autres cartes ici
]
