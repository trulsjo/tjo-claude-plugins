/*
 * Copyright (c) 2026 Example Shop AS.
 * Licensed under the MIT License. See LICENSE in the project root.
 */
#include <atomic>

int next_id() {
    static std::atomic<int> counter{0};
    return ++counter;
}
