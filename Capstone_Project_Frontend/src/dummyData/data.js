export const graphData = [
    {
        "id": "japan",
        "color": "hsl(112, 70%, 50%)",
        width: '20px',
        "data": [
            {
                "x": "1",
                "y": 73
            },
            {
                "x": "2",
                "y": 200
            },
            {
                "x": "3",
                "y": 70
            },
            {
                "x": "4",
                "y": 101
            },
            {
                "x": "5",
                "y": 3
            },
            {
                "x": "6",
                "y": 161
            },
            {
                "x": "7",
                "y": 103
            },
            {
                "x": "8",
                "y": 159
            },
            {
                "x": "9",
                "y": 176
            },
            {
                "x": "10",
                "y": 183
            },
            {
                "x": "11",
                "y": 250
            },
            {
                "x": "12",
                "y": 205
            }
        ]
    }
]

export const predictionGraphData = [
    {
        "id": "france",
        "color": "hsl(192, 70%, 50%)",
        "data": [
            {
                "x": "1",
                "y": 205
            },
            {
                "x": "2",
                "y": 200
            },
            {
                "x": "3",
                "y": 70
            },
            {
                "x": "4",
                "y": 101
            },
            {
                "x": "5",
                "y": 3
            },
            {
                "x": "6",
                "y": 161
            },
            {
                "x": "7",
                "y": 103
            },
            {
                "x": "8",
                "y": 159
            },
            {
                "x": "9",
                "y": 176
            },
            {
                "x": "10",
                "y": 183
            },
            {
                "x": "11",
                "y": 250
            },
            {
                "x": "12",
                "y": 205
            }
        ]
    }
]

export const RechartsDummyData = [
    {
        "x": "1",
        "y": 73,
        "pred": 70
    },
    {
        "x": "2",
        "y": 200,
        "pred": 180
    },
    {
        "x": "3",
        "y": 70,
        "pred": 40
    },
    {
        "x": "4",
        "y": 101,
        "pred": 102
    },
    {
        "x": "5",
        "y": 3,
        "pred": 20
    },
    {
        "x": "6",
        "y": 161,
        "pred": 150
    },
    {
        "x": "7",
        "y": 103,
        "pred": 105
    },
    {
        "x": "8",
        "y": 159,
        "pred": 170
    },
    {
        "x": "9",
        "y": 176,
        "pred": 205
    },
    {
        "x": "10",
        "y": 183,
        "pred": 190
    },
    {
        "x": "11",
        "y": 250,
        "pred": 230
    },
    {
        "x": "12",
        "y": 205,
        "pred": 150
    }
]

export const generateData = (seriesCount, points) => Array(points)
    .fill(1)
    .map((d, i) => ({
        date: new Date(Date.now() - i * 3600000).toDateString(),
        price: Math.max(250, (Math.random() * 3000) | 0),
    }))