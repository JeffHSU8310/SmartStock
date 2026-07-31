#ifndef TAIWAN_QUANT_STORAGE_ENGINE_HPP
#define TAIWAN_QUANT_STORAGE_ENGINE_HPP

#include "../core/types.hpp"
#include <string>
#include <vector>
#include <map>
#include <memory>
#include <mutex>

namespace TaiwanQuant {

class StorageEngine {
public:
    StorageEngine() = default;
    ~StorageEngine() = default;

    // KBar 數據 CRUD
    bool saveKBars(const std::string& symbol, PeriodType period, const std::vector<KBar>& kbars);
    std::vector<KBar> getKBars(const std::string& symbol, PeriodType period, size_t limit = 1000) const;
    bool deleteKBars(const std::string& symbol, PeriodType period);

    // 基本面數據 CRUD
    bool saveFundamental(const FundamentalData& data);
    FundamentalData getFundamental(const std::string& symbol) const;
    bool deleteFundamental(const std::string& symbol);

    // 籌碼面數據 CRUD
    bool saveChip(const ChipData& data);
    ChipData getChip(const std::string& symbol) const;
    bool deleteChip(const std::string& symbol);

    // 消息面數據 CRUD
    bool saveNews(const NewsData& news);
    std::vector<NewsData> getNews(const std::string& symbol = "", size_t limit = 50) const;

    // 取得所有追蹤的標的列表
    std::vector<std::string> getAllSymbols() const;

    // 生成模擬測試數據
    void generateSampleData();

private:
    mutable std::mutex dbMutex_;
    // 記憶體高效索引快取與持久化結構
    std::map<std::string, std::map<int, std::vector<KBar>>> kbarStorage_; // symbol -> period -> kbars
    std::map<std::string, FundamentalData> fundamentalStorage_;
    std::map<std::string, ChipData> chipStorage_;
    std::vector<NewsData> newsStorage_;
};

} // namespace TaiwanQuant

#endif // TAIWAN_QUANT_STORAGE_ENGINE_HPP
