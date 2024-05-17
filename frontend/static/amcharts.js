am5.ready(function() {

    const root = am5.Root.new("chartdiv");
    root.setThemes([
        am5themes_Animated.new(root)
    ]);

    const chart = root.container.children.push(am5percent.PieChart.new(root, {
        layout: root.verticalLayout
    }));

    const series = chart.series.push(am5percent.PieSeries.new(root, {
        valueField: "balance",
        categoryField: "product"
    }));

    balances.map(function (balance) {
        balance.balance = parseFloat(balance.balance)
    })

    series.data.setAll(balances);

    series.ticks.template.setAll({
        stroke: am5.color("#FFFFFF"),
        visible: true
    });

    series.labels.template.setAll({
        fill: am5.color("#FFFFFF")
    });

    series.appear(1000, 100);

});