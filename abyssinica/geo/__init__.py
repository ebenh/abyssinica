import abyssinica.geo.country as country
import abyssinica.geo.region as region
import abyssinica.geo.zone as zone
import abyssinica.geo.city as city

#
#
# Connect Edges
#
#

###########
# COUNTRY #
###########

country.et.make_edge([
    region.et_aa,
    region.et_af,
    region.et_am,
    region.et_be,
    region.et_dd,
    region.et_ga,
    region.et_ha,
    region.et_or,
    region.et_so,
    region.et_sn,
    region.et_ti,
])

##########
# REGION #
##########

region.et_aa.make_edge([
    zone.addis_ababa,
])

region.et_af.make_edge([
    zone.awsi_rasu,
    zone.kilbet_rasu,
    zone.gabi_rasu,
    zone.fantena_rasu,
    zone.hari_rasu,
    zone.argobba,
])

region.et_am.make_edge([
    zone.agew_awi,
    zone.east_gojjam,
    zone.north_gondar,
    zone.north_shewa_et_am,
    zone.north_wello,
    zone.oromia,
    zone.south_gondar,
    zone.south_wollo,
    zone.wag_hemra,
    zone.west_gojjam,
    zone.bahir_dar,
])

region.et_be.make_edge([
    zone.asosa,
    zone.kamashi,
])

region.et_dd.make_edge([
    zone.dire_dawa,
])

region.et_ga.make_edge([
    zone.anuak,
    zone.mezhenger,
    zone.nuer,
])

region.et_ha.make_edge([
    zone.harari,
])

region.et_or.make_edge([
    zone.arsi,
    zone.bale,
    zone.bedele,
    zone.borana,
    zone.east_hararghe,
    zone.east_shewa,
    zone.east_welega,
    zone.guji,
    zone.west_guji,
    zone.horo_gudru_welega,
    zone.illubabor,
    zone.jimma,
    zone.kelem_welega,
    zone.north_shewa_et_or,
    zone.south_west_shewa,
    zone.west_arsi,
    zone.west_hararghe,
    zone.west_shewa,
    zone.west_welega,
    zone.adama,
    zone.jimma,
    zone.oromia_finfinne,
])

region.et_so.make_edge([
    zone.afder,
    zone.jarar,
    zone.nogob,
    zone.gode,
    zone.fafan,
    zone.korahe,
    zone.liben,
    zone.sitti,
    zone.dollo,
])

region.et_sn.make_edge([
    zone.bench_maji,
    zone.dawro,
    zone.gamo_gofa,
    zone.gedeo,
    zone.gurage,
    zone.hadiya,
    zone.keffa,
    zone.kembata_tembaro,
    zone.sheka,
    zone.sidama,
    zone.silte,
    zone.south_omo,
    zone.wolayita,
    zone.alaba,
    zone.amaro,
    zone.basketo,
    zone.burji,
    zone.dirashe,
    zone.konso,
    zone.konta,
    zone.yem,
])

region.et_ti.make_edge([
    zone.central_tigray,
    zone.east_tigray,
    zone.north_west_tigray,
    zone.south_tigray,
    zone.south_east_tigray,
    zone.west_tigray,
    zone.mekele,
])

########
# ZONE #
########

zone.adama.make_edge([city.adama])
zone.addis_ababa.make_edge([city.addis_ababa])
zone.agew_awi.make_edge([city.dangila])
zone.anuak.make_edge([city.gambela])
zone.arsi.make_edge([city.asella])
zone.asosa.make_edge([city.asosa])
zone.bahir_dar.make_edge([city.bahir_dar])
zone.bale.make_edge([city.bale_robe, city.goba, ])
zone.bench_maji.make_edge([city.mizan_teferi])
zone.central_tigray.make_edge([city.aksum])
zone.dire_dawa.make_edge([city.dire_dawa])
zone.east_gojjam.make_edge([city.debre_markos, city.mota, ])
zone.east_hararghe.make_edge([city.alemaya, city.harar, ])
zone.east_shewa.make_edge([city.bishoftu, city.meki, city.modjo, city.ziway])
zone.east_tigray.make_edge([city.adigrat, city.adwa, city.wukro, ])
zone.east_welega.make_edge([city.nekemte])
zone.fafan.make_edge([city.jijiga])
zone.gamo_gofa.make_edge([city.arba_minch, city.sawla, ])
zone.gedeo.make_edge([city.dilla])
zone.gode.make_edge([city.gode])
zone.guji.make_edge([city.negele_borana])
zone.gurage.make_edge([city.butajira, city.welkite, ])
zone.hadiya.make_edge([city.hosaena])
zone.illubabor.make_edge([city.metu])
zone.jarar.make_edge([city.degehabur])
zone.jimma.make_edge([city.agaro, city.jimma, ])
zone.keffa.make_edge([city.bonga])
zone.kelem_welega.make_edge([city.dembi_dolo])
zone.kembata_tembaro.make_edge([city.alaba_kulito, city.durame, ])
zone.mekele.make_edge([city.mekelle])
zone.north_gondar.make_edge([city.gondar])
zone.north_shewa_et_am.make_edge([city.debre_birhan, city.fiche, ])
zone.north_wello.make_edge([city.kobo, city.woldiya, ])
zone.north_west_tigray.make_edge([city.shire])
zone.oromia_finfinne.make_edge([city.burayu, city.sebeta, ])
zone.sheka.make_edge([city.tepi])
zone.sidama.make_edge([city.aleta_wendo, city.hawassa, city.yirgalem, ])
zone.south_gondar.make_edge([city.debre_tabor])
zone.south_omo.make_edge([city.jinka])
zone.south_tigray.make_edge([city.alamata])
zone.south_west_shewa.make_edge([city.woliso])
zone.south_wollo.make_edge([city.dessie, city.kombolcha, ])
zone.west_arsi.make_edge([city.arsi_negele, city.shashamane, ])
zone.west_gojjam.make_edge([city.finote_selam])
zone.west_guji.make_edge([city.bule_hora_town])
zone.west_hararghe.make_edge([city.chiro])
zone.west_shewa.make_edge([city.ambo])
zone.west_welega.make_edge([city.gimbi])
zone.wolayita.make_edge([city.areka, city.boditi, city.sodo, ])