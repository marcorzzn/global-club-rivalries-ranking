const RIVALRIES = [
  {"id": "UEFA_FIO_JUV", "club_a": {"name": "ACF Fiorentina", "short": "FIO", "color": "#4B0082"}, "club_b": {"name": "Juventus FC", "short": "JUV", "color": "#000000"}, "country": "Italy", "confederation": "UEFA", "rivalry_name": "Rivalit\u00e0 Fiorentina-Juventus", "city_derby": false, "h2h": {"total": 95, "w_a": null, "d": null, "w_b": null}, "continuity_blocks": [true, true, true, true, true], "h_dom_score": 85, "h_cont_score": 0, "h_club": {"a": 30, "b": 95}, "i_name": 50, "i_soc": 100, "stadium": {"a": 43147, "b": 41507}, "attendance": {"coverage": 0, "median": null}, "confidence": "MEDIUM"},
  {"id": "UEFA_ROM_JUV", "club_a": {"name": "AS Roma", "short": "ASR", "color": "#8B0000"}, "club_b": {"name": "Juventus FC", "short": "JUV", "color": "#000000"}, "country": "Italy", "confederation": "UEFA", "rivalry_name": "Rivalit\u00e0 Roma-Juventus", "city_derby": false, "h2h": {"total": 102, "w_a": null, "d": null, "w_b": null}, "continuity_blocks": [true, true, true, true, true], "h_dom_score": 90, "h_cont_score": 0, "h_club": {"a": 40, "b": 95}, "i_name": 50, "i_soc": 75, "stadium": {"a": 70634, "b": 41507}, "attendance": {"coverage": 0, "median": null}, "confidence": "MEDIUM"},
  {"id": "UEFA_ROM_NAP", "club_a": {"name": "AS Roma", "short": "ASR", "color": "#8B0000"}, "club_b": {"name": "SSC Napoli", "short": "NAP", "color": "#1FA4D0"}, "country": "Italy", "confederation": "UEFA", "rivalry_name": "Derby del Sole", "city_derby": false, "h2h": {"total": 98, "w_a": null, "d": null, "w_b": null}, "continuity_blocks": [true, true, true, true, true], "h_dom_score": 85, "h_cont_score": 0, "h_club": {"a": 40, "b": 40}, "i_name": 100, "i_soc": 75, "stadium": {"a": 70634, "b": 54726}, "attendance": {"coverage": 0, "median": null}, "confidence": "MEDIUM"},
  {"id": "UEFA_LYO_STE", "club_a": {"name": "Olympique Lyonnais", "short": "LYO", "color": "#FFFFFF"}, "club_b": {"name": "AS Saint-Etienne", "short": "STE", "color": "#008000"}, "country": "France", "confederation": "UEFA", "rivalry_name": "Derby Rh\u00f4ne-Alpes", "city_derby": false, "h2h": {"total": 92, "w_a": null, "d": null, "w_b": null}, "continuity_blocks": [true, true, true, true, true], "h_dom_score": 90, "h_cont_score": 0, "h_club": {"a": 70, "b": 70}, "i_name": 100, "i_soc": 100, "stadium": {"a": 59186, "b": 41965}, "attendance": {"coverage": 0, "median": null}, "confidence": "MEDIUM"},
  {"id": "UEFA_LEE_MAN", "club_a": {"name": "Leeds United", "short": "LEE", "color": "#FFFFFF"}, "club_b": {"name": "Manchester United", "short": "MAN", "color": "#DA291C"}, "country": "England", "confederation": "UEFA", "rivalry_name": "Roses Rivalry", "city_derby": false, "h2h": {"total": 65, "w_a": null, "d": null, "w_b": null}, "continuity_blocks": [true, true, false, true, true], "h_dom_score": 85, "h_cont_score": 0, "h_club": {"a": 30, "b": 95}, "i_name": 100, "i_soc": 100, "stadium": {"a": 37792, "b": 74310}, "attendance": {"coverage": 0, "median": null}, "confidence": "MEDIUM"},
  {
    id: "UEFA_JUV_NAP", club_a: {"name": "Juventus FC", "short": "JUV", "color": "#000000"}, club_b: {"name": "SSC Napoli", "short": "NAP", "color": "#1FA4D0"},
    country: "Italy", confederation: "UEFA", rivalry_name: "Rivalità Juventus-Napoli", city_derby: false,
    h2h: {"total": 105, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 95, h_cont_score: 0, h_club: {"a": 95, "b": 40},
    i_name: 50, i_soc: 100, stadium: {"a": 41507, "b": 54726},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_001", club_a: {"name": "Real Madrid", "short": "REA", "color": "#000000"}, club_b: {"name": "FC Barcelona", "short": "FC ", "color": "#FFFFFF"},
    country: "Spain", confederation: "UEFA", rivalry_name: "El Cl\u00e1sico", city_derby: false,
    h2h: {"total": 182, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 83186, "b": 62652},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_002", club_a: {"name": "Real Madrid", "short": "REA", "color": "#000000"}, club_b: {"name": "Atl\u00e9tico Madrid", "short": "ATL", "color": "#FFFFFF"},
    country: "Spain", confederation: "UEFA", rivalry_name: "El Derbi Madrile\u00f1o", city_derby: true,
    h2h: {"total": 146, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 83186, "b": 70460},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_003", club_a: {"name": "FC Barcelona", "short": "FC ", "color": "#000000"}, club_b: {"name": "RCD Espanyol", "short": "RCD", "color": "#FFFFFF"},
    country: "Spain", confederation: "UEFA", rivalry_name: "Derbi Barcelon\u00ed", city_derby: true,
    h2h: {"total": 116, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 62652, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_004", club_a: {"name": "Sevilla FC", "short": "SEV", "color": "#000000"}, club_b: {"name": "Real Betis", "short": "REA", "color": "#FFFFFF"},
    country: "Spain", confederation: "UEFA", rivalry_name: "El Gran Derbi / Derbi Sevillano", city_derby: true,
    h2h: {"total": 92, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 43883, "b": 60721},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_005", club_a: {"name": "Athletic Club", "short": "ATH", "color": "#000000"}, club_b: {"name": "Real Sociedad", "short": "REA", "color": "#FFFFFF"},
    country: "Spain", confederation: "UEFA", rivalry_name: "Euskal Derbia (Basque Derby)", city_derby: false,
    h2h: {"total": 112, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 53289, "b": 39313},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_006", club_a: {"name": "Liverpool FC", "short": "LIV", "color": "#000000"}, club_b: {"name": "Manchester United", "short": "MAN", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "North West Derby", city_derby: false,
    h2h: {"total": 126, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 61276, "b": 74310},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_007", club_a: {"name": "Liverpool FC", "short": "LIV", "color": "#000000"}, club_b: {"name": "Everton FC", "short": "EVE", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "Merseyside Derby", city_derby: true,
    h2h: {"total": 126, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 61276, "b": 52888},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_008", club_a: {"name": "Arsenal FC", "short": "ARS", "color": "#000000"}, club_b: {"name": "Tottenham Hotspur", "short": "TOT", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "North London Derby", city_derby: true,
    h2h: {"total": 128, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 60704, "b": 62850},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_009", club_a: {"name": "Manchester United", "short": "MAN", "color": "#000000"}, club_b: {"name": "Manchester City", "short": "MAN", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "Manchester Derby", city_derby: true,
    h2h: {"total": 106, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 74310, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_010", club_a: {"name": "Chelsea FC", "short": "CHE", "color": "#000000"}, club_b: {"name": "Arsenal FC", "short": "ARS", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "North West London Derby", city_derby: true,
    h2h: {"total": 126, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40341, "b": 60704},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_011", club_a: {"name": "Manchester United", "short": "MAN", "color": "#000000"}, club_b: {"name": "Chelsea FC", "short": "CHE", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "N/A (Premier League rivalry)", city_derby: false,
    h2h: {"total": 126, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 74310, "b": 40341},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_012", club_a: {"name": "Chelsea FC", "short": "CHE", "color": "#000000"}, club_b: {"name": "Manchester City", "short": "MAN", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "N/A (Modern English clash)", city_derby: false,
    h2h: {"total": 102, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40341, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_013", club_a: {"name": "Liverpool FC", "short": "LIV", "color": "#000000"}, club_b: {"name": "Tottenham Hotspur", "short": "TOT", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "N/A (Top-flight clash)", city_derby: false,
    h2h: {"total": 122, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 61276, "b": 62850},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_014", club_a: {"name": "Newcastle United", "short": "NEW", "color": "#000000"}, club_b: {"name": "Sunderland AFC", "short": "SUN", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "Tyne-Wear Derby", city_derby: false,
    h2h: {"total": 60, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 52305, "b": 49000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_015", club_a: {"name": "Aston Villa", "short": "AST", "color": "#000000"}, club_b: {"name": "Birmingham City", "short": "BIR", "color": "#FFFFFF"},
    country: "England", confederation: "UEFA", rivalry_name: "Second City Derby", city_derby: true,
    h2h: {"total": 46, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 42640, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_016", club_a: {"name": "Celtic FC", "short": "CEL", "color": "#000000"}, club_b: {"name": "Rangers FC", "short": "RAN", "color": "#FFFFFF"},
    country: "Scotland", confederation: "UEFA", rivalry_name: "Old Firm Derby", city_derby: true,
    h2h: {"total": 232, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 60411, "b": 50817},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_017", club_a: {"name": "Heart of Midlothian", "short": "HEA", "color": "#000000"}, club_b: {"name": "Hibernian FC", "short": "HIB", "color": "#FFFFFF"},
    country: "Scotland", confederation: "UEFA", rivalry_name: "Edinburgh Derby", city_derby: true,
    h2h: {"total": 168, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 19852, "b": 20421},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_018", club_a: {"name": "AC Milan", "short": "AC ", "color": "#000000"}, club_b: {"name": "FC Internazionale Milano", "short": "FC ", "color": "#FFFFFF"},
    country: "Italy", confederation: "UEFA", rivalry_name: "Derby della Madonnina", city_derby: true,
    h2h: {"total": 142, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 75817, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_019", club_a: {"name": "Juventus FC", "short": "JUV", "color": "#000000"}, club_b: {"name": "FC Internazionale Milano", "short": "FC ", "color": "#FFFFFF"},
    country: "Italy", confederation: "UEFA", rivalry_name: "Derby d'Italia", city_derby: false,
    h2h: {"total": 136, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 41507, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_020", club_a: {"name": "Juventus FC", "short": "JUV", "color": "#000000"}, club_b: {"name": "Torino FC", "short": "TOR", "color": "#FFFFFF"},
    country: "Italy", confederation: "UEFA", rivalry_name: "Derby della Mole", city_derby: true,
    h2h: {"total": 98, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 41507, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_021", club_a: {"name": "SS Lazio", "short": "SS ", "color": "#000000"}, club_b: {"name": "AS Roma", "short": "AS ", "color": "#FFFFFF"},
    country: "Italy", confederation: "UEFA", rivalry_name: "Derby della Capitale", city_derby: true,
    h2h: {"total": 112, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 70634, "b": 70634},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_022", club_a: {"name": "Genoa CFC", "short": "GEN", "color": "#000000"}, club_b: {"name": "UC Sampdoria", "short": "UC ", "color": "#FFFFFF"},
    country: "Italy", confederation: "UEFA", rivalry_name: "Derby della Lanterna", city_derby: true,
    h2h: {"total": 66, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 33205, "b": 33205},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_023", club_a: {"name": "AC Milan", "short": "AC ", "color": "#000000"}, club_b: {"name": "Juventus FC", "short": "JUV", "color": "#FFFFFF"},
    country: "Italy", confederation: "UEFA", rivalry_name: "N/A (Italian classic)", city_derby: false,
    h2h: {"total": 136, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 75817, "b": 41507},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_024", club_a: {"name": "FC Internazionale Milano", "short": "FC ", "color": "#000000"}, club_b: {"name": "SS Lazio", "short": "SS ", "color": "#FFFFFF"},
    country: "Italy", confederation: "UEFA", rivalry_name: "N/A (Top-flight clash)", city_derby: false,
    h2h: {"total": 110, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 70634},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_025", club_a: {"name": "FC Bayern Munich", "short": "FC ", "color": "#000000"}, club_b: {"name": "Borussia Dortmund", "short": "BOR", "color": "#FFFFFF"},
    country: "Germany", confederation: "UEFA", rivalry_name: "Der Klassiker", city_derby: false,
    h2h: {"total": 118, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 75024, "b": 81365},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_026", club_a: {"name": "Borussia Dortmund", "short": "BOR", "color": "#000000"}, club_b: {"name": "FC Schalke 04", "short": "FC ", "color": "#FFFFFF"},
    country: "Germany", confederation: "UEFA", rivalry_name: "Revierderby", city_derby: false,
    h2h: {"total": 92, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 81365, "b": 62271},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_027", club_a: {"name": "Hamburger SV", "short": "HAM", "color": "#000000"}, club_b: {"name": "SV Werder Bremen", "short": "SV ", "color": "#FFFFFF"},
    country: "Germany", confederation: "UEFA", rivalry_name: "Nordderby", city_derby: false,
    h2h: {"total": 96, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 57000, "b": 42100},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_028", club_a: {"name": "Paris Saint-Germain", "short": "PAR", "color": "#000000"}, club_b: {"name": "Olympique de Marseille", "short": "OLY", "color": "#FFFFFF"},
    country: "France", confederation: "UEFA", rivalry_name: "Le Classique", city_derby: false,
    h2h: {"total": 108, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 47929, "b": 67394},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_029", club_a: {"name": "Olympique Lyonnais", "short": "OLY", "color": "#000000"}, club_b: {"name": "AS Saint-\u00c9tienne", "short": "AS ", "color": "#FFFFFF"},
    country: "France", confederation: "UEFA", rivalry_name: "Le Derby (Derby Rh\u00f4ne-Alpes)", city_derby: false,
    h2h: {"total": 76, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 59186, "b": 41965},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_030", club_a: {"name": "AFC Ajax", "short": "AFC", "color": "#000000"}, club_b: {"name": "Feyenoord Rotterdam", "short": "FEY", "color": "#FFFFFF"},
    country: "Netherlands", confederation: "UEFA", rivalry_name: "De Klassieker", city_derby: false,
    h2h: {"total": 118, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 55865, "b": 47500},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_031", club_a: {"name": "AFC Ajax", "short": "AFC", "color": "#000000"}, club_b: {"name": "PSV Eindhoven", "short": "PSV", "color": "#FFFFFF"},
    country: "Netherlands", confederation: "UEFA", rivalry_name: "De Topper", city_derby: false,
    h2h: {"total": 122, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 55865, "b": 35000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_032", club_a: {"name": "SL Benfica", "short": "SL ", "color": "#000000"}, club_b: {"name": "FC Porto", "short": "FC ", "color": "#FFFFFF"},
    country: "Portugal", confederation: "UEFA", rivalry_name: "O Cl\u00e1ssico", city_derby: false,
    h2h: {"total": 128, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 64642, "b": 50033},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_033", club_a: {"name": "SL Benfica", "short": "SL ", "color": "#000000"}, club_b: {"name": "Sporting CP", "short": "SPO", "color": "#FFFFFF"},
    country: "Portugal", confederation: "UEFA", rivalry_name: "D\u00e9rbi de Lisboa / D\u00e9rbi Eterno", city_derby: true,
    h2h: {"total": 132, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 64642, "b": 50095},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_034", club_a: {"name": "Olympiacos FC", "short": "OLY", "color": "#000000"}, club_b: {"name": "Panathinaikos FC", "short": "PAN", "color": "#FFFFFF"},
    country: "Greece", confederation: "UEFA", rivalry_name: "Derby of the Eternal Enemies", city_derby: true,
    h2h: {"total": 134, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 32115, "b": 16003},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_035", club_a: {"name": "Galatasaray SK", "short": "GAL", "color": "#000000"}, club_b: {"name": "Fenerbah\u00e7e SK", "short": "FEN", "color": "#FFFFFF"},
    country: "Turkey", confederation: "UEFA", rivalry_name: "K\u0131talararas\u0131 Derbi (Intercontinental Derby)", city_derby: true,
    h2h: {"total": 135, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 53798, "b": 47834},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "UEF_036", club_a: {"name": "Real Madrid", "short": "REA", "color": "#000000"}, club_b: {"name": "FC Bayern Munich", "short": "FC ", "color": "#FFFFFF"},
    country: "Spain / Germany", confederation: "UEFA", rivalry_name: "European Cl\u00e1sico", city_derby: false,
    h2h: {"total": 28, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 83186, "b": 75024},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_037", club_a: {"name": "CA Boca Juniors", "short": "CA ", "color": "#000000"}, club_b: {"name": "CA River Plate", "short": "CA ", "color": "#FFFFFF"},
    country: "Argentina", confederation: "CONMEBOL", rivalry_name: "Supercl\u00e1sico", city_derby: true,
    h2h: {"total": 150, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 57200, "b": 85018},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_038", club_a: {"name": "CA Independiente", "short": "CA ", "color": "#000000"}, club_b: {"name": "Racing Club", "short": "RAC", "color": "#FFFFFF"},
    country: "Argentina", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico de Avellaneda", city_derby: true,
    h2h: {"total": 105, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 42069, "b": 51389},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_039", club_a: {"name": "CA San Lorenzo", "short": "CA ", "color": "#000000"}, club_b: {"name": "CA Hurac\u00e1n", "short": "CA ", "color": "#FFFFFF"},
    country: "Argentina", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Porte\u00f1o", city_derby: true,
    h2h: {"total": 88, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 47964, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_040", club_a: {"name": "CA Rosario Central", "short": "CA ", "color": "#000000"}, club_b: {"name": "Newell's Old Boys", "short": "NEW", "color": "#FFFFFF"},
    country: "Argentina", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Rosarino", city_derby: true,
    h2h: {"total": 98, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 46955, "b": 42000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_041", club_a: {"name": "Estudiantes de La Plata", "short": "EST", "color": "#000000"}, club_b: {"name": "Gimnasia LP", "short": "GIM", "color": "#FFFFFF"},
    country: "Argentina", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Platense", city_derby: true,
    h2h: {"total": 86, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_042", club_a: {"name": "CA Boca Juniors", "short": "CA ", "color": "#000000"}, club_b: {"name": "CA Independiente", "short": "CA ", "color": "#FFFFFF"},
    country: "Argentina", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico de Grandes", city_derby: true,
    h2h: {"total": 105, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 57200, "b": 42069},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_043", club_a: {"name": "CR Flamengo", "short": "CR ", "color": "#000000"}, club_b: {"name": "Fluminense FC", "short": "FLU", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Fla-Flu (Cl\u00e1ssico das Multid\u00f5es)", city_derby: true,
    h2h: {"total": 185, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 78838, "b": 78838},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_044", club_a: {"name": "CR Flamengo", "short": "CR ", "color": "#000000"}, club_b: {"name": "CR Vasco da Gama", "short": "CR ", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1ssico dos Milh\u00f5es", city_derby: true,
    h2h: {"total": 175, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 78838, "b": 21880},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_045", club_a: {"name": "CR Flamengo", "short": "CR ", "color": "#000000"}, club_b: {"name": "Botafogo FR", "short": "BOT", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1ssico da Rivalidade", city_derby: true,
    h2h: {"total": 165, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 78838, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_046", club_a: {"name": "CR Vasco da Gama", "short": "CR ", "color": "#000000"}, club_b: {"name": "Fluminense FC", "short": "FLU", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1ssico dos Gigantes", city_derby: true,
    h2h: {"total": 155, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 21880, "b": 78838},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_047", club_a: {"name": "SC Corinthians", "short": "SC ", "color": "#000000"}, club_b: {"name": "SE Palmeiras", "short": "SE ", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Derby Paulista", city_derby: true,
    h2h: {"total": 168, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 49205, "b": 43713},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_048", club_a: {"name": "S\u00e3o Paulo FC", "short": "S\u00c3O", "color": "#000000"}, club_b: {"name": "SC Corinthians", "short": "SC ", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Majestoso", city_derby: true,
    h2h: {"total": 162, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 66795, "b": 49205},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_049", club_a: {"name": "S\u00e3o Paulo FC", "short": "S\u00c3O", "color": "#000000"}, club_b: {"name": "SE Palmeiras", "short": "SE ", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Choque-Rei", city_derby: true,
    h2h: {"total": 160, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 66795, "b": 43713},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_050", club_a: {"name": "Santos FC", "short": "SAN", "color": "#000000"}, club_b: {"name": "SE Palmeiras", "short": "SE ", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1ssico da Saudade", city_derby: false,
    h2h: {"total": 142, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 16068, "b": 43713},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_051", club_a: {"name": "Gr\u00eamio FBPA", "short": "GR\u00ca", "color": "#000000"}, club_b: {"name": "SC Internacional", "short": "SC ", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Grenal", city_derby: true,
    h2h: {"total": 195, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 55662, "b": 50842},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_052", club_a: {"name": "Clube Atl\u00e9tico Mineiro", "short": "CLU", "color": "#000000"}, club_b: {"name": "Cruzeiro EC", "short": "CRU", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1ssico Mineiro", city_derby: true,
    h2h: {"total": 198, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 46000, "b": 61846},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_053", club_a: {"name": "Coritiba FBC", "short": "COR", "color": "#000000"}, club_b: {"name": "Club Athletico Paranaense", "short": "CLU", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Atle-Tiba", city_derby: true,
    h2h: {"total": 165, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_054", club_a: {"name": "EC Bahia", "short": "EC ", "color": "#000000"}, club_b: {"name": "EC Vit\u00f3ria", "short": "EC ", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Ba-Vi", city_derby: true,
    h2h: {"total": 205, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_055", club_a: {"name": "SE Palmeiras", "short": "SE ", "color": "#000000"}, club_b: {"name": "CR Flamengo", "short": "CR ", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1ssico Interestadual / Duelo dos Tit\u00e3s", city_derby: false,
    h2h: {"total": 95, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 43713, "b": 78838},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_056", club_a: {"name": "S\u00e3o Paulo FC", "short": "S\u00c3O", "color": "#000000"}, club_b: {"name": "Athletico Paranaense", "short": "ATH", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "N/A (National clash)", city_derby: false,
    h2h: {"total": 68, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 66795, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_057", club_a: {"name": "SC Internacional", "short": "SC ", "color": "#000000"}, club_b: {"name": "S\u00e3o Paulo FC", "short": "S\u00c3O", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "N/A (National clash)", city_derby: false,
    h2h: {"total": 75, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 50842, "b": 66795},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_058", club_a: {"name": "Clube Atl\u00e9tico Mineiro", "short": "CLU", "color": "#000000"}, club_b: {"name": "Botafogo FR", "short": "BOT", "color": "#FFFFFF"},
    country: "Brazil", confederation: "CONMEBOL", rivalry_name: "N/A (National clash)", city_derby: false,
    h2h: {"total": 85, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 46000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_059", club_a: {"name": "Club Nacional de Football", "short": "CLU", "color": "#000000"}, club_b: {"name": "CA Pe\u00f1arol", "short": "CA ", "color": "#FFFFFF"},
    country: "Uruguay", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Uruguayo", city_derby: true,
    h2h: {"total": 210, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 34000, "b": 40005},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_060", club_a: {"name": "CSD Colo-Colo", "short": "CSD", "color": "#000000"}, club_b: {"name": "Club Universidad de Chile", "short": "CLU", "color": "#FFFFFF"},
    country: "Chile", confederation: "CONMEBOL", rivalry_name: "Supercl\u00e1sico Chileno", city_derby: true,
    h2h: {"total": 128, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 43667, "b": 48665},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_061", club_a: {"name": "Universidad Cat\u00f3lica", "short": "UNI", "color": "#000000"}, club_b: {"name": "Universidad de Chile", "short": "UNI", "color": "#FFFFFF"},
    country: "Chile", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Universitario", city_derby: true,
    h2h: {"total": 126, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 20000, "b": 48665},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_062", club_a: {"name": "Atl\u00e9tico Nacional", "short": "ATL", "color": "#000000"}, club_b: {"name": "Millonarios FC", "short": "MIL", "color": "#FFFFFF"},
    country: "Colombia", confederation: "CONMEBOL", rivalry_name: "El Supercl\u00e1sico Colombiano", city_derby: false,
    h2h: {"total": 118, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 44863, "b": 36343},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_063", club_a: {"name": "Millonarios FC", "short": "MIL", "color": "#000000"}, club_b: {"name": "Independiente Santa Fe", "short": "IND", "color": "#FFFFFF"},
    country: "Colombia", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Capitalino", city_derby: true,
    h2h: {"total": 145, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 36343, "b": 42069},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_064", club_a: {"name": "Atl\u00e9tico Nacional", "short": "ATL", "color": "#000000"}, club_b: {"name": "Independiente Medell\u00edn", "short": "IND", "color": "#FFFFFF"},
    country: "Colombia", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Paisa", city_derby: true,
    h2h: {"total": 155, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 44863, "b": 42069},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_065", club_a: {"name": "Am\u00e9rica de Cali", "short": "AM\u00c9", "color": "#000000"}, club_b: {"name": "Deportivo Cali", "short": "DEP", "color": "#FFFFFF"},
    country: "Colombia", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Vallecaucano", city_derby: true,
    h2h: {"total": 152, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 37899, "b": 42000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_066", club_a: {"name": "Club Universitario", "short": "CLU", "color": "#000000"}, club_b: {"name": "Club Alianza Lima", "short": "CLU", "color": "#FFFFFF"},
    country: "Peru", confederation: "CONMEBOL", rivalry_name: "El Cl\u00e1sico Peruano", city_derby: true,
    h2h: {"total": 155, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 80093, "b": 33938},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_067", club_a: {"name": "Barcelona SC", "short": "BAR", "color": "#000000"}, club_b: {"name": "CS Emelec", "short": "CS ", "color": "#FFFFFF"},
    country: "Ecuador", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico del Astillero", city_derby: true,
    h2h: {"total": 156, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 59283, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_068", club_a: {"name": "Club Olimpia", "short": "CLU", "color": "#000000"}, club_b: {"name": "Club Cerro Porte\u00f1o", "short": "CLU", "color": "#FFFFFF"},
    country: "Paraguay", confederation: "CONMEBOL", rivalry_name: "Supercl\u00e1sico Paraguayo", city_derby: true,
    h2h: {"total": 185, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 19820, "b": 45000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_069", club_a: {"name": "Club Bol\u00edvar", "short": "CLU", "color": "#000000"}, club_b: {"name": "The Strongest", "short": "THE", "color": "#FFFFFF"},
    country: "Bolivia", confederation: "CONMEBOL", rivalry_name: "Cl\u00e1sico Pace\u00f1o", city_derby: true,
    h2h: {"total": 188, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_070", club_a: {"name": "LDU Quito", "short": "LDU", "color": "#000000"}, club_b: {"name": "Fluminense FC", "short": "FLU", "color": "#FFFFFF"},
    country: "Ecuador / Brazil", confederation: "CONMEBOL", rivalry_name: "N/A (Continental rivals)", city_derby: false,
    h2h: {"total": 10, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 41575, "b": 78838},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_071", club_a: {"name": "Al Ahly SC", "short": "AL ", "color": "#000000"}, club_b: {"name": "Zamalek SC", "short": "ZAM", "color": "#FFFFFF"},
    country: "Egypt", confederation: "CAF", rivalry_name: "Cairo Derby", city_derby: true,
    h2h: {"total": 120, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 75000, "b": 75000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_072", club_a: {"name": "Raja Club Athletic", "short": "RAJ", "color": "#000000"}, club_b: {"name": "Wydad AC", "short": "WYD", "color": "#FFFFFF"},
    country: "Morocco", confederation: "CAF", rivalry_name: "Casablanca Derby", city_derby: true,
    h2h: {"total": 115, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 45891},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_073", club_a: {"name": "Esp\u00e9rance de Tunis", "short": "ESP", "color": "#000000"}, club_b: {"name": "Club Africain", "short": "CLU", "color": "#FFFFFF"},
    country: "Tunisia", confederation: "CAF", rivalry_name: "Tunis Derby", city_derby: true,
    h2h: {"total": 115, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 60000, "b": 60000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_074", club_a: {"name": "Esp\u00e9rance de Tunis", "short": "ESP", "color": "#000000"}, club_b: {"name": "\u00c9toile du Sahel", "short": "\u00c9TO", "color": "#FFFFFF"},
    country: "Tunisia", confederation: "CAF", rivalry_name: "Classico Tunisien", city_derby: false,
    h2h: {"total": 118, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 60000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_075", club_a: {"name": "Kaizer Chiefs", "short": "KAI", "color": "#000000"}, club_b: {"name": "Orlando Pirates", "short": "ORL", "color": "#FFFFFF"},
    country: "South Africa", confederation: "CAF", rivalry_name: "Soweto Derby", city_derby: true,
    h2h: {"total": 125, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_076", club_a: {"name": "Mamelodi Sundowns", "short": "MAM", "color": "#000000"}, club_b: {"name": "SuperSport United", "short": "SUP", "color": "#FFFFFF"},
    country: "South Africa", confederation: "CAF", rivalry_name: "Tshwane Derby", city_derby: true,
    h2h: {"total": 70, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_077", club_a: {"name": "Kaizer Chiefs", "short": "KAI", "color": "#000000"}, club_b: {"name": "Mamelodi Sundowns", "short": "MAM", "color": "#FFFFFF"},
    country: "South Africa", confederation: "CAF", rivalry_name: "N/A (Gauteng rivalry)", city_derby: false,
    h2h: {"total": 88, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_078", club_a: {"name": "MC Alger", "short": "MC ", "color": "#000000"}, club_b: {"name": "USM Alger", "short": "USM", "color": "#FFFFFF"},
    country: "Algeria", confederation: "CAF", rivalry_name: "Algiers Derby", city_derby: true,
    h2h: {"total": 90, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_079", club_a: {"name": "JS Kabylie", "short": "JS ", "color": "#000000"}, club_b: {"name": "MC Alger", "short": "MC ", "color": "#FFFFFF"},
    country: "Algeria", confederation: "CAF", rivalry_name: "Le Classico Alg\u00e9rien", city_derby: false,
    h2h: {"total": 92, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_080", club_a: {"name": "CR Belouizdad", "short": "CR ", "color": "#000000"}, club_b: {"name": "MC Alger", "short": "MC ", "color": "#FFFFFF"},
    country: "Algeria", confederation: "CAF", rivalry_name: "Grand Derby Alg\u00e9rois", city_derby: true,
    h2h: {"total": 88, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_081", club_a: {"name": "Asante Kotoko", "short": "ASA", "color": "#000000"}, club_b: {"name": "Hearts of Oak", "short": "HEA", "color": "#FFFFFF"},
    country: "Ghana", confederation: "CAF", rivalry_name: "Ghana Super Clash", city_derby: false,
    h2h: {"total": 82, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_082", club_a: {"name": "TP Mazembe", "short": "TP ", "color": "#000000"}, club_b: {"name": "AS Vita Club", "short": "AS ", "color": "#FFFFFF"},
    country: "DR Congo", confederation: "CAF", rivalry_name: "Cl\u00e1sico Congolais", city_derby: false,
    h2h: {"total": 48, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_083", club_a: {"name": "DC Motema Pembe", "short": "DC ", "color": "#000000"}, club_b: {"name": "AS Vita Club", "short": "AS ", "color": "#FFFFFF"},
    country: "DR Congo", confederation: "CAF", rivalry_name: "Derby de Kinshasa", city_derby: true,
    h2h: {"total": 82, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_084", club_a: {"name": "Al-Hilal Club", "short": "AL-", "color": "#000000"}, club_b: {"name": "Al-Merrikh SC", "short": "AL-", "color": "#FFFFFF"},
    country: "Sudan", confederation: "CAF", rivalry_name: "Omdurman Derby / Sudanese Cl\u00e1sico", city_derby: true,
    h2h: {"total": 112, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_085", club_a: {"name": "Simba SC", "short": "SIM", "color": "#000000"}, club_b: {"name": "Young Africans SC (Yanga)", "short": "YOU", "color": "#FFFFFF"},
    country: "Tanzania", confederation: "CAF", rivalry_name: "Kariakoo Derby", city_derby: true,
    h2h: {"total": 85, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_086", club_a: {"name": "Gor Mahia FC", "short": "GOR", "color": "#000000"}, club_b: {"name": "AFC Leopards", "short": "AFC", "color": "#FFFFFF"},
    country: "Kenya", confederation: "CAF", rivalry_name: "Mashemeji Derby", city_derby: true,
    h2h: {"total": 82, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_087", club_a: {"name": "ASEC Mimosas", "short": "ASE", "color": "#000000"}, club_b: {"name": "Africa Sports", "short": "AFR", "color": "#FFFFFF"},
    country: "Ivory Coast", confederation: "CAF", rivalry_name: "Derby Abidjanais", city_derby: true,
    h2h: {"total": 95, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_088", club_a: {"name": "Al Ahly SC", "short": "AL ", "color": "#000000"}, club_b: {"name": "Esp\u00e9rance de Tunis", "short": "ESP", "color": "#FFFFFF"},
    country: "Egypt / Tunisia", confederation: "CAF", rivalry_name: "N/A (African continental super-clash)", city_derby: false,
    h2h: {"total": 26, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 75000, "b": 60000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_089", club_a: {"name": "Al Ahly SC", "short": "AL ", "color": "#000000"}, club_b: {"name": "Wydad AC", "short": "WYD", "color": "#FFFFFF"},
    country: "Egypt / Morocco", confederation: "CAF", rivalry_name: "N/A (Pan-African rivalry)", city_derby: false,
    h2h: {"total": 13, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 75000, "b": 45891},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CAF_090", club_a: {"name": "Esp\u00e9rance de Tunis", "short": "ESP", "color": "#000000"}, club_b: {"name": "Wydad AC", "short": "WYD", "color": "#FFFFFF"},
    country: "Tunisia / Morocco", confederation: "CAF", rivalry_name: "N/A (North African rivalry)", city_derby: false,
    h2h: {"total": 10, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 60000, "b": 45891},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_091", club_a: {"name": "Al Hilal SFC", "short": "AL ", "color": "#000000"}, club_b: {"name": "Al Nassr FC", "short": "AL ", "color": "#FFFFFF"},
    country: "Saudi Arabia", confederation: "AFC", rivalry_name: "Riyadh Derby", city_derby: true,
    h2h: {"total": 115, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_092", club_a: {"name": "Al Hilal SFC", "short": "AL ", "color": "#000000"}, club_b: {"name": "Al Ittihad FC", "short": "AL ", "color": "#FFFFFF"},
    country: "Saudi Arabia", confederation: "AFC", rivalry_name: "Saudi El Cl\u00e1sico", city_derby: false,
    h2h: {"total": 118, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_093", club_a: {"name": "Al Ahli SFC", "short": "AL ", "color": "#000000"}, club_b: {"name": "Al Ittihad FC", "short": "AL ", "color": "#FFFFFF"},
    country: "Saudi Arabia", confederation: "AFC", rivalry_name: "Jeddah Derby", city_derby: true,
    h2h: {"total": 104, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_094", club_a: {"name": "Al Nassr FC", "short": "AL ", "color": "#000000"}, club_b: {"name": "Al Ittihad FC", "short": "AL ", "color": "#FFFFFF"},
    country: "Saudi Arabia", confederation: "AFC", rivalry_name: "Saudi Cl\u00e1sico", city_derby: false,
    h2h: {"total": 92, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_095", club_a: {"name": "Persepolis FC", "short": "PER", "color": "#000000"}, club_b: {"name": "Esteghlal FC", "short": "EST", "color": "#FFFFFF"},
    country: "Iran", confederation: "AFC", rivalry_name: "Tehran Derby / Red vs Blue", city_derby: true,
    h2h: {"total": 92, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_096", club_a: {"name": "Sepahan SC", "short": "SEP", "color": "#000000"}, club_b: {"name": "Persepolis FC", "short": "PER", "color": "#FFFFFF"},
    country: "Iran", confederation: "AFC", rivalry_name: "El Guilico / Iranian Derby", city_derby: false,
    h2h: {"total": 64, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_097", club_a: {"name": "Sepahan SC", "short": "SEP", "color": "#000000"}, club_b: {"name": "Esteghlal FC", "short": "EST", "color": "#FFFFFF"},
    country: "Iran", confederation: "AFC", rivalry_name: "N/A (Major Iranian clash)", city_derby: false,
    h2h: {"total": 62, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_098", club_a: {"name": "Sepahan SC", "short": "SEP", "color": "#000000"}, club_b: {"name": "Zob Ahan SC", "short": "ZOB", "color": "#FFFFFF"},
    country: "Iran", confederation: "AFC", rivalry_name: "Isfahan Derby", city_derby: true,
    h2h: {"total": 52, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_099", club_a: {"name": "Gamba Osaka", "short": "GAM", "color": "#000000"}, club_b: {"name": "Cerezo Osaka", "short": "CER", "color": "#FFFFFF"},
    country: "Japan", confederation: "AFC", rivalry_name: "Osaka Derby", city_derby: true,
    h2h: {"total": 62, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 39694, "b": 24481},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_100", club_a: {"name": "Yokohama F. Marinos", "short": "YOK", "color": "#000000"}, club_b: {"name": "Kawasaki Frontale", "short": "KAW", "color": "#FFFFFF"},
    country: "Japan", confederation: "AFC", rivalry_name: "Kanagawa Derby", city_derby: true,
    h2h: {"total": 52, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 72327, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_101", club_a: {"name": "Urawa Red Diamonds", "short": "URA", "color": "#000000"}, club_b: {"name": "Gamba Osaka", "short": "GAM", "color": "#FFFFFF"},
    country: "Japan", confederation: "AFC", rivalry_name: "National Derby of Japan", city_derby: false,
    h2h: {"total": 68, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 63700, "b": 39694},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_102", club_a: {"name": "Kashima Antlers", "short": "KAS", "color": "#000000"}, club_b: {"name": "J\u00fabilo Iwata", "short": "J\u00daB", "color": "#FFFFFF"},
    country: "Japan", confederation: "AFC", rivalry_name: "N/A (1990s/2000s J.League rivalry)", city_derby: false,
    h2h: {"total": 64, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40728, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_103", club_a: {"name": "FC Seoul", "short": "FC ", "color": "#000000"}, club_b: {"name": "Suwon Samsung Bluewings", "short": "SUW", "color": "#FFFFFF"},
    country: "South Korea", confederation: "AFC", rivalry_name: "Super Match", city_derby: true,
    h2h: {"total": 103, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 66704, "b": 43959},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_104", club_a: {"name": "Pohang Steelers", "short": "POH", "color": "#000000"}, club_b: {"name": "Ulsan HD FC", "short": "ULS", "color": "#FFFFFF"},
    country: "South Korea", confederation: "AFC", rivalry_name: "Donghaean Derby (East Coast Derby)", city_derby: false,
    h2h: {"total": 145, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 17443, "b": 44102},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_105", club_a: {"name": "Jeonbuk Hyundai Motors", "short": "JEO", "color": "#000000"}, club_b: {"name": "Ulsan HD FC", "short": "ULS", "color": "#FFFFFF"},
    country: "South Korea", confederation: "AFC", rivalry_name: "Hyundai Derby", city_derby: false,
    h2h: {"total": 112, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 42477, "b": 44102},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_106", club_a: {"name": "Sydney FC", "short": "SYD", "color": "#000000"}, club_b: {"name": "Western Sydney Wanderers", "short": "WES", "color": "#FFFFFF"},
    country: "Australia", confederation: "AFC", rivalry_name: "Sydney Derby", city_derby: true,
    h2h: {"total": 44, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 42500, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_107", club_a: {"name": "Melbourne Victory", "short": "MEL", "color": "#000000"}, club_b: {"name": "Melbourne City FC", "short": "MEL", "color": "#FFFFFF"},
    country: "Australia", confederation: "AFC", rivalry_name: "Melbourne Derby", city_derby: true,
    h2h: {"total": 52, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 30050, "b": 30050},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_108", club_a: {"name": "Sydney FC", "short": "SYD", "color": "#000000"}, club_b: {"name": "Melbourne Victory", "short": "MEL", "color": "#FFFFFF"},
    country: "Australia", confederation: "AFC", rivalry_name: "The Big Blue", city_derby: false,
    h2h: {"total": 66, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 42500, "b": 30050},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_109", club_a: {"name": "Adelaide United", "short": "ADE", "color": "#000000"}, club_b: {"name": "Melbourne Victory", "short": "MEL", "color": "#FFFFFF"},
    country: "Australia", confederation: "AFC", rivalry_name: "The Original Rivalry", city_derby: false,
    h2h: {"total": 65, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 30050},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_110", club_a: {"name": "Shanghai Shenhua", "short": "SHA", "color": "#000000"}, club_b: {"name": "Shanghai Port FC", "short": "SHA", "color": "#FFFFFF"},
    country: "China", confederation: "AFC", rivalry_name: "Shanghai Derby", city_derby: true,
    h2h: {"total": 32, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_111", club_a: {"name": "Beijing Guoan", "short": "BEI", "color": "#000000"}, club_b: {"name": "Shanghai Shenhua", "short": "SHA", "color": "#FFFFFF"},
    country: "China", confederation: "AFC", rivalry_name: "Jing-Hu Derby", city_derby: false,
    h2h: {"total": 66, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_112", club_a: {"name": "Al-Zawraa SC", "short": "AL-", "color": "#000000"}, club_b: {"name": "Al-Quwa Al-Jawiya", "short": "AL-", "color": "#FFFFFF"},
    country: "Iraq", confederation: "AFC", rivalry_name: "Iraqi Cl\u00e1sico / Baghdad Derby", city_derby: true,
    h2h: {"total": 82, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_113", club_a: {"name": "Al-Wehdat SC", "short": "AL-", "color": "#000000"}, club_b: {"name": "Al-Faisaly SC", "short": "AL-", "color": "#FFFFFF"},
    country: "Jordan", confederation: "AFC", rivalry_name: "Derby of Jordan / Amman Derby", city_derby: true,
    h2h: {"total": 158, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "AFC_114", club_a: {"name": "Mohun Bagan SG", "short": "MOH", "color": "#000000"}, club_b: {"name": "East Bengal FC", "short": "EAS", "color": "#FFFFFF"},
    country: "India", confederation: "AFC", rivalry_name: "Kolkata Derby / Boro Match", city_derby: true,
    h2h: {"total": 25, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_115", club_a: {"name": "Club Am\u00e9rica", "short": "CLU", "color": "#000000"}, club_b: {"name": "CD Guadalajara (Chivas)", "short": "CD ", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "El S\u00faper Cl\u00e1sico / Cl\u00e1sico Nacional", city_derby: false,
    h2h: {"total": 135, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 83264, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_116", club_a: {"name": "Club Am\u00e9rica", "short": "CLU", "color": "#000000"}, club_b: {"name": "Cruz Azul", "short": "CRU", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "Cl\u00e1sico Joven", city_derby: true,
    h2h: {"total": 142, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 83264, "b": 83264},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_117", club_a: {"name": "Club Am\u00e9rica", "short": "CLU", "color": "#000000"}, club_b: {"name": "Club Universidad Nacional (Pumas)", "short": "CLU", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "Cl\u00e1sico Capitalino", city_derby: true,
    h2h: {"total": 132, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 83264, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_118", club_a: {"name": "CF Monterrey", "short": "CF ", "color": "#000000"}, club_b: {"name": "Tigres UANL", "short": "TIG", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "Cl\u00e1sico Regiomontano (Cl\u00e1sico Regio)", city_derby: true,
    h2h: {"total": 136, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 53500, "b": 41615},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_119", club_a: {"name": "CD Guadalajara", "short": "CD ", "color": "#000000"}, club_b: {"name": "Club Atlas", "short": "CLU", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "Cl\u00e1sico Tapat\u00edo", city_derby: true,
    h2h: {"total": 124, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_120", club_a: {"name": "Cruz Azul", "short": "CRU", "color": "#000000"}, club_b: {"name": "Club Universidad Nacional (Pumas)", "short": "CLU", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "Cl\u00e1sico Chilango", city_derby: true,
    h2h: {"total": 105, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 83264, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_121", club_a: {"name": "CF Monterrey", "short": "CF ", "color": "#000000"}, club_b: {"name": "Santos Laguna", "short": "SAN", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "Duelo del Norte", city_derby: false,
    h2h: {"total": 76, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 53500, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_122", club_a: {"name": "CF Pachuca", "short": "CF ", "color": "#000000"}, club_b: {"name": "Tigres UANL", "short": "TIG", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "CF Pachuca vs Tigres UANL", city_derby: false,
    h2h: {"total": 68, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 41615},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_123", club_a: {"name": "Club Am\u00e9rica", "short": "CLU", "color": "#000000"}, club_b: {"name": "Tigres UANL", "short": "TIG", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "N/A (Modern heavyweight clash)", city_derby: false,
    h2h: {"total": 74, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 83264, "b": 41615},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_124", club_a: {"name": "CF Monterrey", "short": "CF ", "color": "#000000"}, club_b: {"name": "Club Am\u00e9rica", "short": "CLU", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "CF Monterrey vs Club Am\u00e9rica", city_derby: false,
    h2h: {"total": 84, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 53500, "b": 83264},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_125", club_a: {"name": "CF Pachuca", "short": "CF ", "color": "#000000"}, club_b: {"name": "Cruz Azul", "short": "CRU", "color": "#FFFFFF"},
    country: "Mexico", confederation: "CONCACAF", rivalry_name: "Cl\u00e1sico Hidalguense", city_derby: false,
    h2h: {"total": 68, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 83264},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_126", club_a: {"name": "Seattle Sounders FC", "short": "SEA", "color": "#000000"}, club_b: {"name": "Portland Timbers", "short": "POR", "color": "#FFFFFF"},
    country: "USA", confederation: "CONCACAF", rivalry_name: "Cascadia Derby / Cascadia Cup", city_derby: false,
    h2h: {"total": 25, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_127", club_a: {"name": "LA Galaxy", "short": "LA ", "color": "#000000"}, club_b: {"name": "San Jose Earthquakes", "short": "SAN", "color": "#FFFFFF"},
    country: "USA", confederation: "CONCACAF", rivalry_name: "California Cl\u00e1sico", city_derby: false,
    h2h: {"total": 98, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_128", club_a: {"name": "LA Galaxy", "short": "LA ", "color": "#000000"}, club_b: {"name": "Los Angeles FC (LAFC)", "short": "LOS", "color": "#FFFFFF"},
    country: "USA", confederation: "CONCACAF", rivalry_name: "El Tr\u00e1fico", city_derby: true,
    h2h: {"total": 27, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_129", club_a: {"name": "New York Red Bulls", "short": "NEW", "color": "#000000"}, club_b: {"name": "D.C. United", "short": "D.C", "color": "#FFFFFF"},
    country: "USA", confederation: "CONCACAF", rivalry_name: "Atlantic Cup", city_derby: false,
    h2h: {"total": 104, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_130", club_a: {"name": "New York Red Bulls", "short": "NEW", "color": "#000000"}, club_b: {"name": "New York City FC", "short": "NEW", "color": "#FFFFFF"},
    country: "USA", confederation: "CONCACAF", rivalry_name: "Hudson River Derby", city_derby: true,
    h2h: {"total": 34, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_131", club_a: {"name": "Deportivo Saprissa", "short": "DEP", "color": "#000000"}, club_b: {"name": "LD Alajuelense", "short": "LD ", "color": "#FFFFFF"},
    country: "Costa Rica", confederation: "CONCACAF", rivalry_name: "Cl\u00e1sico Nacional de Costa Rica", city_derby: true,
    h2h: {"total": 185, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "CON_132", club_a: {"name": "CSD Municipal", "short": "CSD", "color": "#000000"}, club_b: {"name": "CSD Comunicaciones", "short": "CSD", "color": "#FFFFFF"},
    country: "Guatemala", confederation: "CONCACAF", rivalry_name: "El Cl\u00e1sico Chap\u00edn", city_derby: true,
    h2h: {"total": 185, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 0, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "OFC_133", club_a: {"name": "Auckland City FC", "short": "AUC", "color": "#000000"}, club_b: {"name": "Waitakere United", "short": "WAI", "color": "#FFFFFF"},
    country: "New Zealand", confederation: "OFC", rivalry_name: "Super City Derby / Auckland Derby", city_derby: true,
    h2h: {"total": 62, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "OFC_134", club_a: {"name": "Auckland City FC", "short": "AUC", "color": "#000000"}, club_b: {"name": "Team Wellington", "short": "TEA", "color": "#FFFFFF"},
    country: "New Zealand", confederation: "OFC", rivalry_name: "Capital vs City / NZ Derby", city_derby: false,
    h2h: {"total": 51, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "OFC_135", club_a: {"name": "Ba FC", "short": "BA ", "color": "#000000"}, club_b: {"name": "Lautoka FC", "short": "LAU", "color": "#FFFFFF"},
    country: "Fiji", confederation: "OFC", rivalry_name: "Western Derby / Battle of the Giants", city_derby: false,
    h2h: {"total": 25, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "OFC_136", club_a: {"name": "AS Pirae", "short": "AS ", "color": "#000000"}, club_b: {"name": "AS V\u00e9nus", "short": "AS ", "color": "#FFFFFF"},
    country: "Tahiti (French Polynesia)", confederation: "OFC", rivalry_name: "Le Choc Tahitien / Tahiti Cl\u00e1sico", city_derby: true,
    h2h: {"total": 25, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "OFC_137", club_a: {"name": "AS Magenta", "short": "AS ", "color": "#000000"}, club_b: {"name": "AS Mont-Dore", "short": "AS ", "color": "#FFFFFF"},
    country: "New Caledonia", confederation: "OFC", rivalry_name: "Grand Noum\u00e9a Derby", city_derby: true,
    h2h: {"total": 25, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
  {
    id: "OFC_138", club_a: {"name": "Auckland City FC", "short": "AUC", "color": "#000000"}, club_b: {"name": "AS Pirae", "short": "AS ", "color": "#FFFFFF"},
    country: "New Zealand / Tahiti", confederation: "OFC", rivalry_name: "Auckland City FC vs AS Pirae", city_derby: false,
    h2h: {"total": 4, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 100, h_cont_score: 100, h_club: {"a": 80, "b": 80},
    i_name: 100, i_soc: 75, stadium: {"a": 40000, "b": 40000},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  }
];
module.exports = RIVALRIES;