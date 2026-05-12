// 定义最大页数，比如 3 个 VIS 文件
var maxPages = 8000;  // 修改为实际页面数

// 获取当前文件名
function getCurrentFileName() {
    return window.location.pathname.split("/").pop();
}

// 获取当前文件的编号和类型 (table, nlquery 或 chart)
function getCurrentFileInfo() {
    var currentFile = getCurrentFileName();

    // 正则匹配文件名，提取编号和类型
    var match = currentFile.match(/VIS_(\d+)_(table|nlquery|chart)\.html/);
    if (match) {
        return {
            number: parseInt(match[1]),  // 提取文件编号
            type: match[2]  // 提取类型（table, nlquery 或 chart）
        };
    } else {
        console.error("Filename format not recognized.");
        return null;
    }
}

// 切换到下一个文件
function switchToNextFile() {
    var currentFileInfo = getCurrentFileInfo();

    if (currentFileInfo) {
        var nextNumber = currentFileInfo.number;
        var nextType;

        // 按顺序切换：table -> nlquery -> chart -> 下一页的 table
        if (currentFileInfo.type === "table") {
            nextType = "nlquery";
        } else if (currentFileInfo.type === "nlquery") {
            nextType = "chart";
        } else if (currentFileInfo.type === "chart") {
            nextType = "table";
            nextNumber += 1;  // 增加编号，切换到下一个文件
        }

        // 如果超出了最大编号，则循环回第一个文件
        if (nextNumber > maxPages) {
            nextNumber = 1;
        }

        // 生成下一个文件的名称
        var nextFile = "VIS_" + nextNumber + "_" + nextType + ".html";

        // 跳转到下一个文件
        window.location.href = nextFile;
    }
}

// 监听 Enter 键，按下时切换到下一个文件
document.addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        switchToNextFile();
    }
});

// 居中页面内容并限制高度，避免溢出
function centerContent() {
    // 修改 body 的样式，使内容居中
    document.body.style.display = 'flex';
    document.body.style.justifyContent = 'center';
    document.body.style.alignItems = 'center';
    document.body.style.height = '100vh';  // 设置高度为视口高度
    document.body.style.margin = '0';  // 移除默认的边距

    // 确保 body 可以滚动
    document.body.style.overflowY = 'auto';

    // 获取当前文件信息
    var currentFileInfo = getCurrentFileInfo();
    var containers = document.querySelectorAll('.container, .vis-container');

    // 根据文件类型设置不同的宽度和高度
    if (currentFileInfo && currentFileInfo.type === 'chart') {
        // 如果是 chart 页面，设置较窄的 max-width 和较高的 max-height
        containers.forEach(function(container) {
            container.style.margin = '0';  // 清除原有的边距
            container.style.maxWidth = '30%';  // 设置较窄的宽度
            container.style.maxHeight = '300vh';  // 设置较高的高度
            // container.style.overflowY = 'auto';  // 超出时启用滚动条
            container.style.zoom = '1.2';  // 放大
        });
    } else {
        // 对于其他类型页面（如 table 和 nlquery），设置较宽的宽度
        containers.forEach(function(container) {
            container.style.margin = '0';  // 清除原有的边距
            container.style.maxWidth = '90%';  // 设置较宽的宽度
            container.style.maxHeight = '90vh';  // 限制高度，防止内容溢出
            container.style.overflowY = 'auto';  // 超出时启用滚动条
        });
    }
}

// 在页面加载时调用
window.onload = centerContent;
