#include <cstddef>
#include <deque>
#include <string>

void evict(std::deque<std::string>& entries, std::size_t max_entries) {
    // FIXME JIRA-881: evict by total size in bytes, not by entry count
    while (entries.size() > max_entries) entries.pop_front();
}
