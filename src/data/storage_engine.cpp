#include "storage_engine.hpp"
#include <algorithm>
#include <random>

namespace TaiwanQuant {

bool StorageEngine::saveKBars(const std::string& symbol, PeriodType period, const std::vector<KBar>& kbars) {
    std::lock_guard<std::mutex> lock(dbMutex_);
    int periodKey = static_cast<int>(period);
    auto& targetVector = kbarStorage_[symbol][periodKey];
    targetVector = kbars;
    return true;
}

std::vector<KBar> StorageEngine::getKBars(const std::string& symbol, PeriodType period, size_t limit) const {
    std::lock_guard<std::mutex> lock(dbMutex_);
    int periodKey = static_cast<int>(period);
    auto symIt = kbarStorage_.find(symbol);
    if (symIt == kbarStorage_.end()) return {};

    auto perIt = symIt->second.find(periodKey);
    if (perIt == symIt->second.end()) return {};

    const auto& kbars = perIt->second;
    if (kbars.size() <= limit) {
        return kbars;
    }
    return std::vector<KBar>(kbars.end() - limit, kbars.end());
}

bool StorageEngine::deleteKBars(const std::string& symbol, PeriodType period) {
    std::lock_guard<std::mutex> lock(dbMutex_);
    int periodKey = static_cast<int>(period);
    auto symIt = kbarStorage_.find(symbol);
    if (symIt != kbarStorage_.end()) {
        symIt->second.erase(periodKey);
        return true;
    }
    return false;
}

bool StorageEngine::saveFundamental(const FundamentalData& data) {
    std::lock_guard<std::mutex> lock(dbMutex_);
    fundamentalStorage_[data.symbol] = data;
    return true;
}

FundamentalData StorageEngine::getFundamental(const std::string& symbol) const {
    std::lock_guard<std::mutex> lock(dbMutex_);
    auto it = fundamentalStorage_.find(symbol);
    if (it != fundamentalStorage_.end()) {
        return it->second;
    }
    return FundamentalData{symbol, "2026-07-31", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
}

bool StorageEngine::deleteFundamental(const std::string& symbol) {
    std::lock_guard<std::mutex> lock(dbMutex_);
    return fundamentalStorage_.erase(symbol) > 0;
}

bool StorageEngine::saveChip(const ChipData& data) {
    std::lock_guard<std::mutex> lock(dbMutex_);
    chipStorage_[data.symbol] = data;
    return true;
}

ChipData StorageEngine::getChip(const std::string& symbol) const {
    std::lock_guard<std::mutex> lock(dbMutex_);
    auto it = chipStorage_.find(symbol);
    if (it != chipStorage_.end()) {
        return it->second;
    }
    return ChipData{symbol, "2026-07-31", 0, 0, 0, 0, 0, 0, 0};
}

bool StorageEngine::deleteChip(const std::string& symbol) {
    std::lock_guard<std::mutex> lock(dbMutex_);
    return chipStorage_.erase(symbol) > 0;
}

bool StorageEngine::saveNews(const NewsData& news) {
    std::lock_guard<std::mutex> lock(dbMutex_);
    newsStorage_.push_back(news);
    return true;
}

std::vector<NewsData> StorageEngine::getNews(const std::string& symbol, size_t limit) const {
    std::lock_guard<std::mutex> lock(dbMutex_);
    std::vector<NewsData> result;
    for (auto it = newsStorage_.rbegin(); it != newsStorage_.rend(); ++it) {
        if (symbol.empty() || it->symbol == symbol) {
            result.push_back(*it);
            if (result.size() >= limit) break;
        }
    }
    return result;
}

std::vector<std::string> StorageEngine::getAllSymbols() const {
    std::lock_guard<std::mutex> lock(dbMutex_);
    std::vector<std::string> symbols;
    for (const auto& kv : kbarStorage_) {
        symbols.push_back(kv.first);
    }
    return symbols;
}

void StorageEngine::generateSampleData() {
    std::vector<std::string> sampleSymbols = {"2330.TW", "2454.TW", "2317.TW", "TX00.FITX"};
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> noise(-0.02, 0.025);

    for (const auto& sym : sampleSymbols) {
        double currentPrice = (sym == "TX00.FITX") ? 22500.0 : ((sym == "2330.TW") ? 980.0 : 1200.0);
        std::vector<KBar> dailyKBars;
        
        for (int i = 120; i >= 0; --i) {
            double changePct = noise(rng);
            double open = currentPrice;
            double close = open * (1.0 + changePct);
            double high = std::max(open, close) * (1.0 + std::abs(noise(rng)) * 0.5);
            double low = std::min(open, close) * (1.0 - std::abs(noise(rng)) * 0.5);
            int64_t volume = static_cast<int64_t>(10000 + std::abs(noise(rng)) * 500000);

            KBar kbar{"2026-07-31", open, high, low, close, volume, close * volume};
            dailyKBars.push_back(kbar);
            currentPrice = close;
        }
        saveKBars(sym, PeriodType::DAILY, dailyKBars);

        // 建立基本面範例
        FundamentalData fund{
            sym, "2026-07-31",
            215000.0, 5.2, 18.6, // 營收與YoY
            38.5, 24.5, 5.2,     // EPS, PE, PB
            28.5, 16.2, 53.5,    // ROE, ROA, 毛利率
            2.8                   // 殖利率
        };
        saveFundamental(fund);

        // 建立籌碼面範例
        ChipData chip{
            sym, "2026-07-31",
            12500, 3200, -800,   // 外資, 投信, 自營商
            45000, 3200, 7.1,    // 融資, 融券, 券資比
            72.5                  // 大股東持股比
        };
        saveChip(chip);
    }

    // 消息面範例 (填滿 7 個欄位: id, timestamp, symbol, title, content, source, sentimentScore)
    saveNews(NewsData{"N001", "2026-07-31 09:30:00", "2330.TW", "台積電先進製程訂單爆滿", "法人看好全年獲利再創新高，先進封裝產能供不應求。", "經濟日報", 0.85});
    saveNews(NewsData{"N002", "2026-07-31 10:15:00", "TX00.FITX", "聯準會維持利率不變", "全球科技股大漲帶動台指期強勢走高，多頭情緒高漲。", "中央社", 0.75});
}

} // namespace TaiwanQuant
