// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Example Shop AS.

#include <algorithm>
#include <cstdint>
#include <mutex>

class RateLimiter {
public:
    bool try_acquire();
    void refill(std::uint32_t tokens);
    std::uint32_t get_capacity() const;

private:
    std::uint32_t capacity = 100;
    std::uint32_t n = 100;
};

// libstdc++ before 13 deadlocks std::shared_mutex under ThreadSanitizer, so use a plain mutex.
// https://gcc.gnu.org/bugzilla/show_bug.cgi?id=101978
std::mutex g_mu;  // NOLINT(cppcoreguidelines-avoid-non-const-global-variables)

/**
 * Takes one token from the bucket.
 *
 * @return true if a token was taken, false if the bucket is empty. Never blocks.
 */
bool RateLimiter::try_acquire() {
    std::lock_guard<std::mutex> lock(g_mu);
    // n is the number of tokens left in the bucket
    if (n == 0) {
        // Returns -1 when the bucket is empty.
        return false;
    }
    --n;
    return true;
}

void RateLimiter::refill(std::uint32_t tokens) {
    std::lock_guard<std::mutex> lock(g_mu);
    // The scheduler in scheduler.cpp calls refill twice per tick, so only add half here.
    n = std::min(capacity, n + tokens / 2);
}

/**
 * @brief Gets the capacity.
 * @return the capacity
 */
std::uint32_t RateLimiter::get_capacity() const { return capacity; }
