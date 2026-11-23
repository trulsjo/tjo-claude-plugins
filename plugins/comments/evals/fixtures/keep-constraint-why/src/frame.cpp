#include <cstddef>
#include <vector>

std::vector<unsigned char> make_frame(std::size_t payload_size) {
    // The radio firmware reads frames in 64-byte blocks and rejects a partial block.
    std::size_t padded = (payload_size + 63) / 64 * 64;
    return std::vector<unsigned char>(padded, 0);
}
