
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.covariance.empirical import _emp_pcov_init,merge_emp_scov, _emp_pcov_update
from precise.synthetic.generate import create_correlated_dataset


def test_onlineempirical():
    data = create_correlated_dataset(10000, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    conventional_mean = np.mean(data, axis=0)
    conventional_cov = np.cov(data, rowvar=False)
    conventional_corrcoef = np.corrcoef(data, rowvar=False)
    ocov = _emp_pcov_init(n_dim=data.shape[1])
    for observation in data:
        ocov = _emp_pcov_update(s=ocov, x=observation)
    assert np.isclose(conventional_mean, ocov['mean']).all(), \
        """
        Mean should be the same with both approaches.
        """
    assert np.isclose(conventional_cov, ocov['pcov'], atol=1e-3).all(), \
        """
        Covariance-matrix should be the same with both approaches.
        """
    from precise.covariance.util import cov_to_corrcoef
    ocorr = cov_to_corrcoef(ocov['pcov'])
    assert np.isclose(conventional_corrcoef, ocorr).all(), \
        """
        Pearson-Correlationcoefficient-matrix should be the same with both approaches.
        """


def test_merging():
    data_part1 = create_correlated_dataset(500, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]), (1, 5, 3))
    data_part2 = create_correlated_dataset( \
        1000, (5, 6, 2), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]), (1, 5, 3))
    ocov_part1 = _emp_pcov_init(n_dim=3)
    ocov_part2 = _emp_pcov_init(n_dim=3)
    ocov_both = _emp_pcov_init(n_dim=3)

    for row in data_part1:
        ocov_part1 = _emp_pcov_update(s=ocov_part1, x=row)
        ocov_both = _emp_pcov_update(s=ocov_both, x=row)

    for row in data_part2:
        ocov_part2 = _emp_pcov_update(s=ocov_part2, x=row)
        ocov_both = _emp_pcov_update(s=ocov_both, x=row)

    ocov_merged = merge_emp_scov(s=ocov_part1, other_s=ocov_part2)
    assert ocov_both['n_samples'] == ocov_merged['n_samples']
    assert np.isclose(ocov_both['mean'], ocov_merged['mean']).all()
    assert np.isclose(ocov_both['pcov'], ocov_merged['pcov']).all()


if __name__=='__main__':
    test_onlineempirical()
    test_merging()