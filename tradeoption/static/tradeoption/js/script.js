function drawChart() {
	// fetch("/trade/tradenow/data")
	// .then(res => res.json())
	// .then(data => {
	// 	console.log(data);

	d3.json('/trade/tradenow/data').then(function (prices) {
		console.log(prices);

		const months = {
			0: 'Jan',
			1: 'Feb',
			2: 'Mar',
			3: 'Apr',
			4: 'May',
			5: 'Jun',
			6: 'Jul',
			7: 'Aug',
			8: 'Sep',
			9: 'Oct',
			10: 'Nov',
			11: 'Dec'
		}

		var timestamp = [];
		var dateFormat = d3.timeParse("%Y-%m-%d %H:%M:%S");
		for (var price of Object.keys(prices)) {
			timestamp.push(dateFormat(price));
			// prices[i]['TIMESTAMP'] = dateFormat(prices[i]['TIMESTAMP'])
		}

		const margin = {
				top: 15,
				right: 65,
				bottom: 205,
				left: 50
			},
			w = 500 - margin.left - margin.right,
			h = 320 - margin.top - margin.bottom;

		var svg = d3.select("#container")
			.attr("width", w + margin.left + margin.right)
			.attr("height", h + margin.top + margin.bottom)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		let dates = _.map(prices, 'TIMESTAMP');

		var xmin = d3.min(timestamp.map(r => r.getTime()));
		var xmax = d3.max(timestamp.map(r => r.getTime()));
		var xScale = d3.scaleLinear().domain([-1, timestamp.length - 1])
			.range([0, w])
		var xDateScale = d3.scaleQuantize().domain([0, timestamp.length]).range(timestamp)
		let xBand = d3.scaleBand().domain(d3.range(-1, dates.length)).range([0, w]).padding(0.3)
		var xAxis = d3.axisBottom()
			.scale(xScale)
			.tickFormat(function (d) {
				console.log("----------------");
				console.log(d);
				d = timestamp[d]

				hours = d.getHours()
				minutes = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes()
				amPM = hours < 13 ? 'am' : 'pm'
				return d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear()
			});

		svg.append("rect")
			.attr("id", "rect")
			.attr("width", w)
			.attr("height", h)
			.style("fill", "none")
			.style("pointer-events", "all")
			.attr("clip-path", "url(#clip)")

		var gX = svg.append("g")
			.attr("class", "axis x-axis") //Assign "axis" class
			.attr("transform", "translate(0," + h + ")")
			.call(xAxis)

		gX.selectAll(".tick text")
			.call(wrap, xBand.bandwidth())

		var ymin = d3.min(Object.keys(prices).map(r => prices[r]['3. low']));
		var ymax = d3.max(Object.keys(prices).map(r => prices[r]['2. high']));
		var yScale = d3.scaleLinear().domain([ymin, ymax]).range([h, 0]).nice();
		var yAxis = d3.axisLeft()
			.scale(yScale)

		var gY = svg.append("g")
			.attr("class", "axis y-axis")
			.call(yAxis);

		var chartBody = svg.append("g")
			.attr("class", "chartBody")
			.attr("clip-path", "url(#clip)");

		// draw rectangles
		let candles = chartBody.selectAll(".candle")
			.data(Object.keys(prices))
			.enter()
			.append("rect")
			.attr('x', (d, i) => xScale(i) - xBand.bandwidth())
			.attr("class", "candle")
			.attr('y', d => yScale(Math.max(prices[d]['1. open'], prices[d]['4. close'])))
			.attr('width', xBand.bandwidth())
			.attr('height', d => (prices[d]['1. open'] === prices[d]['4. close']) ? 1 : yScale(Math.min(prices[d]['1. open'], prices[d]['4. close'])) - yScale(Math.max(prices[d]['1. open'], prices[d]['4. close'])))
			.attr("fill", d => (prices[d]['1. open'] === prices[d]['4. close'] ? "silver" : (prices[d]['1. open'] > prices[d]['4. close']) ? "red" : "green"));


		// draw high and low
		let stems = chartBody.selectAll("g.line")
			.data(Object.keys(prices))
			.enter()
			.append("line")
			.attr("class", "stem")
			.attr("x1", (d, i) => xScale(i) - xBand.bandwidth() / 2)
			.attr("x2", (d, i) => xScale(i) - xBand.bandwidth() / 2)
			.attr("y1", d => yScale(prices[d]['2. high']))
			.attr("y2", d => yScale(prices[d]['3. low']))
			.attr("stroke", d => (prices[d]['1. open'] === prices[d]['4. close']) ? "white" : (prices[d]['1. open'] > prices[d]['4. close']) ? "red" : "green");

		svg.append("defs")
			.append("clipPath")
			.attr("id", "clip")
			.append("rect")
			.attr("width", w)
			.attr("height", h)

		const extent = [
			[0, 0],
			[w, h]
		];

		var resizeTimer;
		var zoom = d3.zoom()
			.scaleExtent([.5, 20])
			.translateExtent(extent)
			.extent(extent)
			.on("zoom", zoomed)
			.on('zoom.end', zoomend);

		svg.call(zoom)

		function zoomed() {

			var t = d3.event.transform;
			let xScaleZ = t.rescaleX(xScale);

			let hideTicksWithoutLabel = function () {
				d3.selectAll('.xAxis .tick text').each(function (d) {
					if (this.innerHTML === '') {
						this.parentNode.style.display = 'none'
					}
				})
			}

			gX.call(
				d3.axisBottom(xScaleZ).tickFormat((d, e, target) => {
					if (d >= 0 && d <= dates.length - 1) {
						d = timestamp[d]
						hours = d.getHours()
						minutes = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes()
						amPM = hours < 13 ? 'am' : 'pm'
						return d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear()
					}
				})
			)

			candles.attr("x", (d, i) => xScaleZ(i) - (xBand.bandwidth() * t.k) / 2)
				.attr("width", xBand.bandwidth() * t.k)
				.attr('y', d => yScale(Math.max(prices[d]['1. open'], prices[d]['4. close'])))
				.attr('height', d => (prices[d]['1. open'] === prices[d]['4. close']) ? 1 : yScale(Math.min(prices[d]['1. open'], prices[d]['4. close'])) - yScale(Math.max(prices[d]['1. open'], prices[d]['4. close'])));

			stems.attr("x1", (d, i) => xScaleZ(i) - xBand.bandwidth() / 2 + xBand.bandwidth() * 0.5);
			stems.attr("x2", (d, i) => xScaleZ(i) - xBand.bandwidth() / 2 + xBand.bandwidth() * 0.5);
			stems.attr("y1", d => yScale(prices[d]['2. high']));
			stems.attr("y2", d => yScale(prices[d]['3. low']));
			hideTicksWithoutLabel();

			gX.selectAll(".tick text")
				.call(wrap, xBand.bandwidth())

		}

		function zoomend() {
			var t = d3.event.transform;
			let xScaleZ = t.rescaleX(xScale);
			clearTimeout(resizeTimer)
			resizeTimer = setTimeout(function () {

				var xmin = new Date(xDateScale(Math.floor(xScaleZ.domain()[0])))
				xmax = new Date(xDateScale(Math.floor(xScaleZ.domain()[1])))
				filtered = _.filter(Object.keys(prices), d => ((d >= xmin) && (d <= xmax)))
				minP = +d3.min(filtered, d => prices[d]['3. low'])
				maxP = +d3.max(filtered, d => prices[d]['2. high'])
				buffer = Math.floor((maxP - minP) * 0.1)

				yScale.domain([minP - buffer, maxP + buffer])
				candles.transition()
					.duration(800)
					.attr("y", (d) => yScale(Math.max(prices[d]['1. open'], prices[d]['4. close'])))
					.attr("height", d => (prices[d]['1. open'] === prices[d]['4. close']) ? 1 : yScale(Math.min(prices[d]['1. open'], prices[d]['4. close'])) - yScale(Math.max(prices[d]['1. open'], prices[d]['4. close'])));

				stems.transition().duration(800)
					.attr("y1", (d) => yScale(prices[d]['2. high']))
					.attr("y2", (d) => yScale(prices[d]['3. low']))

				gY.transition().duration(800).call(d3.axisLeft().scale(yScale));

			}, 500)

		}
	});
	// })
}

function wrap(text, width) {
	text.each(function () {
		var text = d3.select(this),
			words = text.text().split(/\s+/).reverse(),
			word,
			line = [],
			lineNumber = 0,
			lineHeight = 1.1, // ems
			y = text.attr("y"),
			dy = parseFloat(text.attr("dy")),
			tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
		while (word = words.pop()) {
			line.push(word);
			tspan.text(line.join(" "));
			if (tspan.node().getComputedTextLength() > width) {
				line.pop();
				tspan.text(line.join(" "));
				line = [word];
				tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
			}
		}
	});
}

drawChart();