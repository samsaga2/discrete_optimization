#include <iostream>
#include <fstream>
#include <vector>
#include <optional>
#include <algorithm>

struct Item {
    int index;
    int value{0};
    int weight{0};
};

struct Node {
    int depth{0};
    std::vector<bool> taken;
    int room{0};
    int value{0};
    double estimation{0};
};

int capacity;
std::vector<Item> items;
std::vector<Item> sorted_items;
std::optional<Node> best_found_node;

double calc_estimation(int item_offset, int capacity) {
    int value = 0;
    int weight = 0;
    for(auto i = 0; i < sorted_items.size(); i++) {
        const auto& item = sorted_items[i];
        if(item.index < item_offset)
            continue;
        if(weight+item.weight <= capacity) {
            value += item.value;
            weight += item.weight;
        } else {
            double remaining = capacity - weight;
            value += (item.value / (double)item.weight) * remaining;
            break;
        }
    }
    return value;
}

void read_data(std::ifstream& is) {
    int item_count;

    is >> item_count >> capacity;
    for(auto i = 0; i < item_count; i++) {
        auto item = Item{.index = i};
        is >> item.value >> item.weight;
        items.emplace_back(std::move(item));
    }
}

void traverse_graph(const Node& node) {
    if(node.depth <= items.size()) {
        const auto& child_item = items[node.depth];
        /* std::cout << "node depth " << node.depth << " value " << node.value << " room " << node.room << " estimation " << node.estimation << std::endl; */
        /* std::cout << "item " << child_item.index << " value " << child_item.value << " weight " << child_item.weight << std::endl; */
        
        // left node
        auto left_room = node.room - child_item.weight;
        if(left_room >= 0) {
            auto left_taken = node.taken;
            left_taken[node.depth+1] = true;

            auto left_value = node.value + child_item.value;
            auto estimation = calc_estimation(node.depth+1, left_room) + left_value;
            /* std::cout << "estimation " << calc_estimation(child_item.index, left_room) << " value " << left_value << " capacity " << left_room << " room " << node.room << std::endl; */
            if(estimation > best_found_node->value) {
                auto left_node = Node{
                    .depth = node.depth + 1,
                    .taken = std::move(left_taken),
                    .room = left_room,
                    .value = left_value,
                    .estimation = estimation,
                };
                traverse_graph(left_node);
            }
        }

        // right node
        if(node.estimation > best_found_node->value) {
            auto estimation = calc_estimation(node.depth+1, node.room) + node.value;
            auto right_node = Node{
                .depth = node.depth + 1,
                .taken = node.taken,
                .room = node.room,
                .value = node.value,
                .estimation = estimation,
            };
            traverse_graph(right_node);
        }
    } else {
        if(!best_found_node.has_value() || best_found_node->value < node.value) {
            best_found_node = node;
            /* std::cout << "best node depth " << node.depth << " value " << node.value << " estimation " << node.estimation << " room " << node.room << std::endl; */
        }
    }
}

int main(int argc, char** argv) {
    if(argc <= 1)
        return -1;

    auto is = std::ifstream(argv[1]);
    read_data(is);
    is.close();

    sorted_items = items;
    std::sort(sorted_items.begin(), sorted_items.end(),
              [](const auto & i, const auto& j) {
                  auto ii = i.value/(double)i.weight;
                  auto jj = j.value/(double)j.weight;
                  return ii > jj;
              });

    auto root_node = Node{.room = capacity};
    root_node.estimation = calc_estimation(0, capacity);
    root_node.taken.resize(items.size());
    traverse_graph(root_node);

    if(best_found_node.has_value()) {
        std::cout << best_found_node->value << " \0" << std::endl;
        for(auto i : best_found_node->taken)
            std::cout << (i?"1":"0") << ' ';
        std::cout << std::endl;
    } else {
        std::cerr << "Not solved" << std::endl;
    }

    return 0;
}

