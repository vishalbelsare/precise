


import re
import pandas as pd
import numpy as np


def to_elo_frame(elos):
    """
       Construct a dataframe where regressors are inferred from manager names.
    """
    MODEL_KEY_REPLACEMENTS = {'gamma': 'g','t0':'tzero'}
    MODEL_KEYS_NOT_USED = ['manager', 'manger', 'long', 'pcov', 'check']

    def augment_alloc(name):
        # Differentiate between 2nd and 3rd hints (usually alloc verus portfolio method)
        splt = name.split('_')
        if splt[2] == splt[1]:
            splt[2] = splt[2] + 'xx'  # Allocation
            splt[1] = splt[1] + 'xy'  # Portfolio
        return '_'.join(splt)

    def infer_categorical_and_ordinal(elos):
        categorical = set()
        ordinal = set()
        for name, (_elo, _cpu) in elos:
            name = augment_alloc(name=name)
            name_words = name.split('_')
            for wd in name_words:
                for r_old, r_new in MODEL_KEY_REPLACEMENTS.items():
                    wd = wd.replace(r_old, r_new)
                wd_head = re.search("[^\d]*", wd).group()
                if wd == wd_head:
                    if wd not in MODEL_KEYS_NOT_USED:
                        categorical.add(wd_head)
                else:
                    ordinal.add(wd_head)
        return categorical, ordinal

    def make_model_regs_elo(elos, categorical, ordinal):
        model_reg_elo = list()
        for name, (elo,cpu) in elos:
            name = augment_alloc(name=name)
            name_words = name.split('_')
            reg_pairs = list()
            for wd in list(set(name_words)):
                for r_old,r_new in MODEL_KEY_REPLACEMENTS.items():
                    wd = wd.replace(r_old,r_new)

                if wd in categorical:
                    pair = (wd+'_hot',1)
                else:
                    wd_head = re.search("[^\d]*", wd).group()
                    if wd_head in categorical:
                        pair = (wd+'_hot',1)
                    elif wd_head in ordinal:
                        wd_tail = wd[len(wd_head):]
                        pair = (wd_head+'_ord',float(wd_tail))
                    else:
                        pair = None
                if pair is not None:
                    reg_pairs.append(pair)
            model_reg_elo.append( (name, reg_pairs, elo) )
        return model_reg_elo

    def model_regs_elo_keys(model_regs_elo):
        kys = set()
        for model, regs, _elo in model_regs_elo:
            for k, v in regs:
                kys.add(k)
        return kys

    def model_regs_elo_to_frame(model_regs_elo):
        """
            Convert tuples into dataframe setting non-ordinal variables to 0.0
        """
        kys = model_regs_elo_keys(model_regs_elo)

        rows = list()
        for model, regs, elo in model_regs_elo:
            row_dict = dict([(k, np.nan if '_ord' in k else 0.0) for k in kys])
            row_dict.update({'elo': elo})
            for reg, val in regs:
                row_dict[reg] = val
            row = pd.DataFrame.from_dict(row_dict, orient='index').transpose()
            rows.append(row)
        df = pd.concat(rows)
        return df

    categorical, ordinal = infer_categorical_and_ordinal(elos)
    models_and_regs = make_model_regs_elo(elos=elos, categorical=categorical, ordinal=ordinal)
    df = model_regs_elo_to_frame(model_regs_elo=models_and_regs)
    return df



if __name__=='__main__':
    elos = [('schur_vol_vol_ewa_r050_n25_s5_g050_long_manager',
             (1603.7297195060585, None)),
            ('schur_weak_weak_pm_t0_r050_n25_s5_g000_long_manager',
             (1600.8406929729617, None)),
            ('schur_weak_weak_pm_t0_r025_n50_s5_g100_long_manager',
             (1599.369350006955, None)),
            ('schur_weak_weak_ewa_r050_n25_s5_g010_long_manager',
             (1599.0661492833633, None)),
            ('rp_ewa_r05_p0_long_manager', (1596.3373833978706, None)),
            ('schur_weak_vol_ewa_r050_n25_s5_g100_long_manager',
             (1594.930109646238, None)),
            ('ppo_ewa_d0_r025_n50_vol_long_manager',
             (1592.7100151772393, None)),
            ('hrp_weak_vol_ewa_r025_n50_s50_long_manager',
             (1592.5667006894428, None)),
            ('schur_weak_weak_ewa_r050_n25_s5_g000_long_manager',
             (1591.9705027103919, None)),
            ('schur_weak_vol_ewa_r050_n25_s5_g050_long_manager',
             (1590.106223700346, None)),
            ('schur_weak_weak_ewa_r050_n25_s5_g100_long_manager',
             (1589.65347072206, None)),
            ('molyboga_r025_n50_long_manager', (1589.235020220747, None)),
            ('schur_weak_weak_ewa_r025_n50_s5_g100_long_manager',
             (1585.0042343819182, None)),
            ('rp_ewa_r05_p60_long_manager', (1582.0085501511626, None)),
            ('schur_weak_vol_ewa_r050_n25_s5_g000_long_manager',
             (1580.4753228404468, None)),
            ('schur_weak_weak_ewa_r050_n25_s25_g100_h150_long_manager',
             (1579.1762716546548, None)),
            ('schur_vol_vol_ewa_r050_n25_s5_g010_long_manager',
             (1575.9150616540876, None)),
            ('schur_weak_weak_ewa_r025_n50_s5_g010_long_manager',
             (1573.9010159333845, None)),
            ('schur_diag_weak_pm_t0_r050_n25_s5_g010_l21_long_manager',
             (1570.7455778982433, None)),
            ('schur_weak_weak_pm_t0_r025_n50_s100_g100_h500_long_manager',
             (1568.8164020519625, None)),
            ('rp_ewa_r02_p80_long_manager', (1565.9793093542116, None)),
            ('schur_weak_weak_ewa_r050_n25_s25_g100_h500_long_manager',
             (1565.6877907861217, None)),
            ('schur_weak_vol_ewa_r050_n25_s5_g010_long_manager',
             (1565.1739624987015, None)),
            ('schur_weak_weak_pm_t0_r025_n50_s5_g050_long_manager',
             (1560.6438914721064, None)),
            ('schur_weak_weak_ewa_r050_n25_s5_g050_long_manager',
             (1560.577551037039, None)),
            ('rp_ewa_r01_p60_long_manager', (1560.2173987797178, None)),
            ('slurp_vol_r025_s5_p20_g100_long_manager',
             (1559.2289300226655, None)),
            ('rp_ewa_r05_p20_long_manager', (1556.990107646616, None)),
            ('schur_weak_weak_pm_t0_r050_n25_s100_g100_h500_long_manager',
             (1553.8045522314446, None)),
            ('slurp_vol_r001_s25_p20_g100_long_manger',
             (1553.4783588612092, None)),
            ('hrp_vol_vol_pm_t0_d0_r025_n50_s5_long_manager',
             (1553.4013078622518, None)),
            ('schur_weak_weak_pm_t0_r050_n25_s25_g100_h500_long_manager',
             (1550.8775582156472, None)),
            ('rp_ewa_r02_p20_long_manager', (1550.303028550498, None)),
            ('schur_weak_weak_ewa_r050_n25_s100_g100_h500_long_manager',
             (1549.7777251993728, None)),
            ('molyboga_r025_s25_gamma000_long_manager',
             (1548.1560831583809, None)),
            ('schur_weak_weak_pm_t0_r025_n50_s5_g000_long_manager',
             (1548.0304881518277, None)),
            ('schur_weak_weak_pm_t0_r025_n50_s5_g010_long_manager',
             (1547.937758538328, None)),
            ('schur_weak_weak_ewa_r050_n25_s25_g100_h125_long_manager',
             (1547.8599560241548, None)),
            ('schur_weak_weak_pm_t0_r025_n50_s25_g100_h125_long_manager',
             (1547.7871298838559, None)),
            ('schur_weak_weak_ewa_r025_n50_s25_g100_h125_long_manager',
             (1544.260587360124, None)),
            ('schur_vol_vol_ewa_r050_n25_s5_g000_long_manager',
             (1542.7553567689206, None)),
            ('rp_ewa_r01_p20_l21_long_manager', (1542.4304811804334, None)),
            ('rp_ewa_r05_p61_long_manager', (1541.8476100699693, None)),
            ('schur_weak_weak_ewa_r025_n50_s5_g050_long_manager',
             (1541.63255250041, None)),
            ('rp_ewa_r02_p60_long_manager', (1541.2829630559143, None)),
            ('schur_weak_weak_ewa_r025_n50_s5_g000_long_manager',
             (1540.2724440022268, None)),
            ('ppo_sk_lw_pcov_d1_n100_vol_long_manager',
             (1536.3351845887885, None)),
            ('molyboga_r025_s25_gamma100_long_manager',
             (1535.9498863670724, None)),
            ('weak_pm_t0_d0_r025_n50_h500_long_manager',
             (1533.0690946820262, None)),
            ('rp_ewa_r02_p40_long_manager', (1530.2446069216392, None)),
            ('schur_weak_weak_pm_t0_r025_n50_s25_g100_h500_long_manager',
             (1529.1963937631199, None)),
            ('schur_weak_weak_pm_t0_r025_n50_s25_g100_h150_long_manager',
             (1526.4079111989652, None)),
            ('schur_weak_weak_ewa_r025_n50_s100_g100_h500_long_manager',
             (1523.0108623997928, None)),
            ('ppo_sk_glcv_pcov_d0_n100_sharpe_long_manager',
             (1522.1750539391119, 1222.945114850998)),
            ('schur_weak_weak_ewa_r025_n50_s25_g100_h500_long_manager',
             (1521.9226394598372, None)),
            ('ppo_sk_mcd_pcov_d0_n100_sharpe_long_manager',
             (1520.3022979460268, 39.70094704627991)),
            ('schur_weak_vol_ewa_r001_n200_s50_g100_l20_long_manager',
             (1518.8008004163958, None)),
            ('weak_pm_t0_d0_r050_n50_h500_long_manager',
             (1516.5882404677793, None)),
            ('schur_weak_weak_pm_t0_r050_n25_s25_g100_h125_long_manager',
             (1515.7218729951433, None)),
            ('slurp_vol_r025_s25_p20_g000_long_manager',
             (1514.9559591465193, None)),
            ('molyboga_r025_s5_gamma000_long_manager',
             (1512.9494518493163, None)),
            ('rp_weak_pm_t0_p40_l21_long_manager',
             (1511.9745726722713, None)),
            ('ppo_sk_glcv_pcov_d0_n100_t0_vol_long_manager',
             (1510.8165481325102, 708.6874990463257)),
            ('schur_vol_vol_pm_t0_d0_r025_n50_s25_g100_long_manager',
             (1510.3981709405177, None)),
            ('rp_ewa_r01_p59_long_manager', (1509.7242736429776, None)),
            ('rp_ewa_r01_p80_long_manager', (1508.90171999332, None)),
            ('rp_ewa_r01_p40_l20_long_manager', (1508.3691867192697, None)),
            ('ppo_sk_mcd_pcov_d0_n100_quad_long_manager',
             (1507.8241574505146, 49.152095317840576)),
            ('hrp_weak_vol_ewa_r025_n50_s50_l10_long_manager',
             (1506.91729196244, None)),
            ('rp_ewa_r01_p0_long_manager', (1505.430355774904, None)),
            ('schur_weak_weak_pm_t0_r050_n25_s25_g100_h150_long_manager',
             (1501.7683980640984, None)),
            ('ppo_sk_lw_pcov_d0_n100_sharpe_long_manager',
             (1501.059852102078, None)),
            ('rp_ewa_r01_p40_l21_long_manager', (1499.9577039735195, None)),
            ('weak_ewa_t0_d0_r050_n50_h500_long_manager',
             (1497.4774466707165, None)),
            ('ppo_pm_t0_d0_r025_n50_sharpe_long_manager',
             (1495.8049466204218, 39.30381226539612)),
            ('schur_weak_weak_ewa_r025_n50_s25_g100_h150_long_manager',
             (1494.5834739141321, None)),
            ('equal_long_manager', (1494.1122405475735, None)),
            ('schur_weak_weak_pm_t0_r050_n25_s5_g050_long_manager',
             (1493.045622214821, None)),
            ('slurp_vol_r001_s25_p20_g000_long_manger',
             (1492.788775384805, None)),
            ('hrp_weak_weak_pm_t0_d0_r025_n50_s5_long_manager',
             (1492.1445387529523, None)),
            ('schur_vol_vol_ewa_r050_n25_s5_g100_long_manager',
             (1491.5299553309576, None)),
            ('rp_ewa_r02_p0_long_manager', (1491.1642541500867, None)),
            ('slurp_vol_r025_s100_p20_g000_long_manager',
             (1490.6093109062822, None)),
            ('weak_ewa_t0_d0_r025_n50_long_manager',
             (1490.0746714419274, 37.15584444999695)),
            ('rp_ewa_r01_p61_long_manager', (1489.8537415440644, None)),
            ('weak_pm_t0_d0_r050_n50_h125_long_manager',
             (1489.5945068706042, None)),
            ('molyboga_r025_n50_s100_long_manager',
             (1489.1469325855826, None)),
            ('schur_diag_diag_ewa_r050_n25_s5_g100_long_manager',
             (1488.6416093964, None)),
            ('schur_weak_weak_pm_t0_r050_n25_s5_g010_long_manager',
             (1487.4081050680547, None)),
            ('ppo_sk_glcv_pcov_d0_n100_vol_long_manager',
             (1486.9624424693975, 372.40891790390015)),
            ('schur_diag_weak_pm_t0_r050_n25_s5_g000_long_manager',
             (1486.709593583904, None)),
            ('equal_check_long_manager', (1486.481536896077, None)),
            ('ppo_sk_glcv_pcov_d0_n100_t0_sharpe_long_manager',
             (1484.868794783575, 522.7344714403152)),
            ('weak_sk_lw_pcov_d0_n100_long_manager',
             (1484.8170414029555, None)),
            ('molyboga_r025_n50_s25_long_manager',
             (1484.5326150292772, None)),
            ('rp_ewa_r05_p40_long_manager', (1482.9978369581138, None)),
            ('molyboga_r001_n100_long_manger', (1482.1281391901557, None)),
            ('slurp_vol_r001_s100_p20_g000_long_manger',
             (1481.6229566246582, None)),
            ('rp_weak_pm_t0_r01_p40_l20_long_manager',
             (1479.882738061665, None)),
            ('schur_diag_weak_pm_t0_r050_n25_s5_g010_long_manager',
             (1478.6875652668302, None)),
            ('schur_weak_vol_ewa_r001_n200_s50_g100_l21_long_manager',
             (1477.6652103947195, None)),
            ('weak_ewa_t0_d0_r025_n50_h125_long_manager',
             (1476.7945931764375, None)),
            ('schur_vol_vol_pm_t0_d0_r025_n50_s50_g100_long_manager',
             (1475.3065920527365, None)),
            ('molyboga_r001_s100_gamma100_long_manger',
             (1473.1396044319602, None)),
            ('molyboga_r001_n100_s100_long_manger',
             (1472.2043696484566, None)),
            ('slurp_vol_r001_s100_p20_g100_long_manger',
             (1471.5452316170245, None)),
            ('ldp_s25_n50_long_manager', (1469.1394626928136, None)),
            ('schur_diag_weak_pm_t0_r050_n25_s5_g050_long_manager',
             (1469.1020406050443, None)),
            ('ppo_sk_mcd_pcov_d0_n100_vol_long_manager',
             (1468.9221642587381, 230.10923790931702)),
            ('rp_ewa_r01_p40_long_manager', (1468.6861558208084, None)),
            ('weak_ewa_t0_d0_r025_n50_h500_long_manager',
             (1467.546168775907, None)),
            ('schur_weak_weak_pm_t0_r050_n25_s5_g100_long_manager',
             (1465.8401634436182, None)),
            ('schur_vol_vol_pm_t0_d0_r025_n50_s5_g100_long_manager',
             (1464.950881790425, None)),
            ('schur_diag_weak_pm_t0_r050_n25_s5_g100_long_manager',
             (1464.4171853592645, None)),
            ('weak_pm_t0_d0_r025_n50_long_manager',
             (1463.7147664190684, None)),
            ('ppo_sk_glcv_pcov_d0_n100_t0_quad_long_manager',
             (1463.4279811901185, 556.1878499190012)),
            ('ppo_ewa_d0_r025_n50_quad_long_manager',
             (1462.2377954505116, 71.01052606105804)),
            ('weak_sk_glcv_pcov_d0_n100_t0_long_manager',
             (1461.8861132689085, 297.68794572353363)),
            ('weak_sk_mcd_pcov_d0_n100_long_manager',
             (1460.6887891771842, 123.25749707221985)),
            ('rp_ewa_r01_p20_l20_long_manager', (1457.8476251835218, None)),
            ('weak_ewa_t0_d0_r050_n50_long_manager',
             (1457.838448805113, 39.41439235210419)),
            ('ppo_sk_lw_pcov_d0_n100_quad_long_manager',
             (1456.902899199652, None)),
            ('rp_ewa_r05_p80_long_manager', (1456.607741111099, None)),
            ('weak_sk_glcv_pcov_d0_n100_long_manager',
             (1453.3099627302813, 570.7869900465012)),
            ('molyboga_r001_s25_gamma000_long_manger',
             (1451.840156056914, None)),
            ('ldp_s5_n100_long_manager', (1451.6108297672051, None)),
            ('weak_pm_t0_d0_r025_n50_h125_long_manager',
             (1451.3575463090363, None)),
            ('rp_ewa_r02_p59_long_manager', (1451.2217468742474, None)),
            ('hrp_vol_vol_pm_t0_d0_r025_n50_s50_long_manager',
             (1450.0776895668043, None)),
            ('slurp_vol_r001_s5_p20_g100_long_manger',
             (1449.994499244418, None)),
            ('slurp_vol_r001_s5_p20_g000_long_manger',
             (1448.6860497250084, None)),
            ('ppo_pm_t0_d0_r025_n50_vol_long_manager',
             (1446.2907221960845, 23.043459335962932)),
            ('ldp_s5_n50_long_manager', (1445.3501748770016, None)),
            ('molyboga_r001_s100_gamma000_long_manger',
             (1445.3377741904212, None)),
            ('schur_diag_weak_pm_t0_r050_n25_s5_g010_l11_long_manager',
             (1445.111912386923, None)),
            ('rp_ewa_r02_p61_long_manager', (1443.3815977717209, None)),
            ('slurp_vol_r025_s5_p20_g000_long_manager',
             (1441.6915729006578, None)),
            ('slurp_vol_r025_s100_p20_g100_long_manager',
             (1437.5450847605046, None)),
            ('rp_ewa_r01_p20_long_manager', (1436.1383145129896, None)),
            ('ppo_sk_glcv_pcov_d0_n100_quad_long_manager',
             (1435.1197514800215, 585.8880656957626)),
            ('molyboga_r001_s5_gamma100_long_manger',
             (1433.665986529887, None)),
            ('molyboga_r025_s100_gamma100_long_manager',
             (1419.6209394119057, None)),
            ('weak_pm_t0_d0_r050_n50_long_manager',
             (1419.087923084258, 34.10416221618652)),
            ('slurp_vol_r025_s25_p20_g100_long_manager',
             (1417.4153281087251, None)),
            ('molyboga_r025_s5_gamma100_long_manager',
             (1416.5840473887563, None)),
            ('rp_ewa_r05_p59_long_manager', (1410.8069005574137, None)),
            ('ppo_ewa_d0_r025_n50_sharpe_long_manager',
             (1410.7809958637106, 75.59677314758301)),
            ('molyboga_r025_s100_gamma000_long_manager',
             (1403.322707369863, None)),
            ('molyboga_r001_s5_gamma000_long_manger',
             (1402.9976227275536, None)),
            ('ldp_s25_n100_long_manager', (1396.9014736799404, None)),
            ('molyboga_r001_s25_gamma100_long_manger',
             (1388.589307468737, None)),
            ('schur_diag_diag_ewa_r050_n25_s5_g050_long_manager',
             (1379.2794618084897, None)),
            ('schur_diag_diag_ewa_r050_n25_s5_g010_long_manager',
             (1368.7394036852604, None)),
            ('ppo_pm_t0_d0_r025_n50_quad_long_manager',
             (1361.0812012139434, 23.093345046043396)),
            ('schur_diag_diag_ewa_r050_n25_s5_g000_long_manager',
             (1335.2527948305578, None))]
    df = to_elo_frame(elos)
    print(df[:5])

