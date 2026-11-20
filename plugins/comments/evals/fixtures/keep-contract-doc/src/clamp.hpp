#pragma once

/**
 * Clamps a percentage to the range 0 to 100.
 *
 * @param pct  any value, in percent; NaN is treated as 0.
 * @return pct limited to [0, 100].
 */
double clamp_percent(double pct);
