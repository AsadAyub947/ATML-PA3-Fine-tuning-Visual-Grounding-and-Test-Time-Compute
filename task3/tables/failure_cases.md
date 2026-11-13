## MATH: selection disagreements (SC vs SelfCert+RWC, N=32, order 0)

- q=test:2460 gold=154 | SC → 58 (✗) | SelfCert+RWC → 154 (✓) | votes {'154': 11, '58': 11, 'NO_ANSWER': 3, '45': 1, '98': 1}
- q=test:2892 gold=-71 | SC → 1 (✗) | SelfCert+RWC → 0 (✗) | votes {'0': 4, '1': 4, '23': 2, '-1': 1, 'NO_ANSWER': 1}
- q=test:2948 gold=1+\sqrt 2,\ 1-\sqrt 2,\ 2+\sqrt 3,\ 2-\sqrt 3 | SC → 1 (✗) | SelfCert+RWC → 2 + \sqrt{3}, 2 - \sqrt{3}, \frac{3 + \sqrt{13 + 4\sqrt{3}}}{2}, \frac{3 - \sqrt{13 + 4\sqrt{3}}}{2}, \frac{3 + \sqrt{13 - 4\sqrt{3}}}{2}, \frac{3 - \sqrt{13 - 4\sqrt{3}}}{2} (✗) | votes {'1': 5, '1 \\text{ and } 2': 4, '2 + \\sqrt{3}, 2 - \\sqrt{3}': 3, '2 + \\sqrt{3}, 2 - \\sqrt{3}, \\frac{3 + \\sqrt{13 + 4\\sqrt{3}}}{2}, \\frac{3 - \\sqrt{13 + 4\\sqrt{3}}}{2}, \\frac{3 + \\sqrt{13 - 4\\sqrt{3}}}{2}, \\frac{3 - \\sqrt{13 - 4\\sqrt{3}}}{2}': 3, 'NO_ANSWER': 2}

## MATH: premature stops (agreement policy) later fixed by fixed-32 SC

- q=test:2460 order=7 stopped at n=4 with '58' (gold 154); pool correct fraction 0.34
- q=test:534 order=6 stopped at n=4 with '48' (gold 56); pool correct fraction 0.72
- q=test:3409 order=4 stopped at n=8 with '0' (gold 3); pool correct fraction 0.66

## MathVista: selection disagreements (SC vs VisConf+RWC, N=32, order 0)

- q=552 gold=4 | SC → 4 (✓) | VisConf+RWC → 2 (✗) | votes {'4': 14, '3': 9, '2': 9}
- q=643 gold=A | SC → C (✗) | VisConf+RWC → A (✓) | votes {'C': 11, 'A': 10, 'NO_ANSWER': 8, 'D': 3}
- q=313 gold=10 | SC → INVALID:10-20 years (✗) | VisConf+RWC → 20 (✗) | votes {'INVALID:10-15 years': 5, '10': 5, 'INVALID:10-20 years': 5, '20': 4, '0': 3}

## MathVista: premature stops (agreement policy) later fixed by fixed-32 SC

- q=358 order=4 stopped at n=4 with 'D' (gold A); pool correct fraction 0.44
- q=821 order=4 stopped at n=4 with 'B' (gold A); pool correct fraction 0.66
- q=434 order=0 stopped at n=4 with 'C' (gold A); pool correct fraction 0.53

## Live refinement transitions (all W→C and C→W cases are listed in tables/live_revision_cases.json)

- q=test:4702 C→W: initial=59 → revised=None (gold 59)
- q=test:916 W→C: initial=12 → revised=14 (gold 14)