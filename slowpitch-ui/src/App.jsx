import { useState, useEffect } from "react";
import "./App.css";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ReferenceLine,
  LabelList,
} from "recharts";

function formatNumber(value, digits = 2) {
  if (value === null || value === undefined || Number.isNaN(value)) return "-";
  return Number(value).toFixed(digits);
}

function PlayerComparisonCard({ player }) {
  return (
    <div className="comparison-card">
      <h4>{player.PLAYER}</h4>
      <span className="pill">{player.archetype}</span>

      <div className="metric-list">
        <div>
          <span>OV</span>
          <strong>{formatNumber(player.offensive_value, 1)}</strong>
        </div>
        <div>
          <span>OV/PA</span>
          <strong>{formatNumber(player.value_per_pa)}</strong>
        </div>
        <div>
          <span>Hit Rate</span>
          <strong>{formatNumber(player.hit_rate)}</strong>
        </div>
        <div>
          <span>XBH Rate</span>
          <strong>{formatNumber(player.xbh_rate)}</strong>
        </div>
        <div>
          <span>Out Rate</span>
          <strong>{formatNumber(player.out_rate)}</strong>
        </div>
      </div>
    </div>
  );
}

function PerformanceTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;

  const p = payload[0].payload;

  return (
    <div className="chart-tooltip">
      <strong>{p.PLAYER}</strong>
      <div>Archetype: {p.archetype}</div>
      <div>OV/PA: {formatNumber(p.value_per_pa)}</div>
      <div>Hit Rate: {formatNumber(p.hit_rate)}</div>
      <div>XBH Rate: {formatNumber(p.xbh_rate)}</div>
      <div>Out Rate: {formatNumber(p.out_rate)}</div>
    </div>
  );
}

function PerformanceChart({ data, onPlayerClick }) {
  const avgHit =
    data.reduce((sum, p) => sum + Number(p.hit_rate || 0), 0) / data.length;

  const avgValue =
    data.reduce((sum, p) => sum + Number(p.value_per_pa || 0), 0) / data.length;

  const chartData = data.filter(
    (p) => p.PLAYER && p.hit_rate !== null && p.value_per_pa !== null
  );

  return (
    <div className="chart-shell">
      <div className="chart-note">
        Right = better contact. Up = more offensive value. Dotted lines show team averages.
      </div>

      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={420}>
          <ScatterChart margin={{ top: 24, right: 32, bottom: 24, left: 12 }}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              type="number"
              dataKey="hit_rate"
              name="Hit Rate"
              tickFormatter={(v) => v.toFixed(2)}
              domain={["dataMin - 0.03", "dataMax + 0.03"]}
            />

            <YAxis
              type="number"
              dataKey="value_per_pa"
              name="OV/PA"
              tickFormatter={(v) => v.toFixed(2)}
              domain={["dataMin - 0.10", "dataMax + 0.10"]}
            />

            <ReferenceLine x={avgHit} strokeDasharray="5 5" />
            <ReferenceLine y={avgValue} strokeDasharray="5 5" />

            <Tooltip content={<PerformanceTooltip />} />

            <Scatter
              data={chartData}
              fill="#18395f"
              onClick={(point) => onPlayerClick?.(point.PLAYER)}
            >
              <LabelList
                dataKey="PLAYER"
                position="top"
                className="chart-label"
              />
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      <div className="quadrant-grid">
        <div>
          <strong>Top Right:</strong> Best overall profiles
        </div>
        <div>
          <strong>Top Left:</strong> Productive but less contact-driven
        </div>
        <div>
          <strong>Bottom Right:</strong> Contact without enough value
        </div>
        <div>
          <strong>Bottom Left:</strong> Lower efficiency group
        </div>
      </div>
    </div>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [playerA, setPlayerA] = useState("");
  const [playerB, setPlayerB] = useState("");
  const [editableLineup, setEditableLineup] = useState([]);

  const handleUpload = async () => {
    if (!file) {
      setError("Please choose a CSV file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("league_name", file.name.replace(".csv", ""));
    formData.append("league_code", "UPL");

    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/analyze`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Analysis failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }

    useEffect(() => {
      if (result?.batting_order) {
        setEditableLineup(result.batting_order);
      }
    }, [result]);


  };

  const movePlayer = (index, direction) => {
    const newLineup = [...editableLineup];
    const newIndex = index + direction;

    if (newIndex < 0 || newIndex >= newLineup.length) return;

    [newLineup[index], newLineup[newIndex]] = [
      newLineup[newIndex],
      newLineup[index],
    ];

    setEditableLineup(newLineup);
  };

  const recalculateRuns = async () => {
  setLoading(true);

  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/simulate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lineup: editableLineup,
      }),
    });

    const data = await res.json();

    setResult((prev) => ({
      ...prev,
      simulation_results: data,
    }));
  } catch (err) {
    setError("Simulation failed");
  } finally {
    setLoading(false);
  }
};

  const topPlayers = result?.leaderboard?.slice(0, 12) ?? [];
  const allPlayers = result?.leaderboard ?? [];
  const selectedA = allPlayers.find((p) => p.PLAYER === playerA);
  const selectedB = allPlayers.find((p) => p.PLAYER === playerB);
  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">
            Softball Analytics Engine</p>
          <h1>Slowpitch Performance Lab</h1>
          <p className="subtitle">
            Upload a GameChanger CSV to generate player evaluations, optimized batting orders,
            and scouting-style team insights.
          </p>
        </div>
      </header>

      <section className="upload-card">
        <div>
          <h2>Analyze Team Data</h2>
          <p>Select a GameChanger batting export to run the model.</p>
        </div>


        {!result && !loading && (
          <p className="muted">
            Upload a CSV or download the sample file to get started.
          </p>
        )}


        <div className="upload-row">
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
          <button onClick={handleUpload} disabled={loading}>
            {loading ? "Waking analytics engine (up to 60s)..." : "Analyze CSV"}
          </button>


          <a href="/sample-data.csv" download="sample.csv">
            <button style={{ marginLeft: 10 }}>
              Download Sample CSV
            </button>
          </a>
        </div>

        {file && <p className="file-name">Selected: {file.name}</p>}
        {error && <p className="error">{error}</p>}
      </section>

      {result && (
        <main className="results">
          <section className="section-heading">
            <p className="eyebrow">Report</p>
            <h2>{result.league}</h2>
          </section>

          <section className="grid two-col">
            <div className="card">
              <h3>Top Players</h3>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Player</th>
                      <th>OV</th>
                      <th>OV/PA</th>
                      <th>Hit%</th>
                      <th>Archetype</th>
                    </tr>
                  </thead>
                  <tbody>
                    {topPlayers.map((p, i) => (
                      <tr key={`${p.PLAYER}-${i}`}>
                        <td className="player-name">{p.PLAYER}</td>
                        <td>{formatNumber(p.offensive_value, 1)}</td>
                        <td>{formatNumber(p.value_per_pa)}</td>
                        <td>{formatNumber(p.hit_rate)}</td>
                        <td>
                          <span className="pill">{p.archetype}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="lineup">
              {editableLineup.map((p, i) => (
                <div className="lineup-row" key={p.PLAYER}>
                  <div className="order-number">{i + 1}</div>

                  <div>
                    <div className="player-name">{p.PLAYER}</div>
                    <div className="muted">
                      {p.batting_role} · OV/PA {formatNumber(p.value_per_pa)}
                    </div>
                  </div>

                  <div className="lineup-controls">
                    <button onClick={() => movePlayer(i, -1)}>↑</button>
                    <button onClick={() => movePlayer(i, 1)}>↓</button>
                  </div>
                </div>
              ))}


              <button onClick={recalculateRuns}>
                Recalculate Runs
              </button>
            </div>
          </section>



          <p className="muted">
            Based on 1000 simulated 7-inning games using player outcome probabilities.
          </p>
          {result.simulation_results && (
            <section className="card">
              <h3>Run Projection</h3>
              <p>Average Runs: {formatNumber(result.simulation_results.avg_runs, 1)}</p>
              <p>
                Range: {result.simulation_results.min_runs} - {result.simulation_results.max_runs}
              </p>
              <p>Median: {result.simulation_results.median_runs}</p>
            </section>
          )}


          <section className="card">
            <h3>Player Performance Map</h3>
            <PerformanceChart
              data={result.leaderboard}
              onPlayerClick={(name) => {
                if (!playerA) {
                  setPlayerA(name);
                } else {
                  setPlayerB(name);
                }
              }}
            />
          </section>
          <section className="card">
            <h3>Team Analysis</h3>
            <pre className="report">{result.report}</pre>
          </section>


          <section className="card">
            <h3>Player Comparison</h3>

            <div className="comparison-controls">
              <select value={playerA} onChange={(e) => setPlayerA(e.target.value)}>
                <option value="">Select Player A</option>
                {allPlayers.map((p) => (
                  <option key={`a-${p.PLAYER}`} value={p.PLAYER}>
                    {p.PLAYER}
                  </option>
                ))}
              </select>

              <select value={playerB} onChange={(e) => setPlayerB(e.target.value)}>
                <option value="">Select Player B</option>
                {allPlayers.map((p) => (
                  <option key={`b-${p.PLAYER}`} value={p.PLAYER}>
                    {p.PLAYER}
                  </option>
                ))}
              </select>
            </div>

            {selectedA && selectedB && (
              <div className="comparison-grid">
                <PlayerComparisonCard player={selectedA} />
                <PlayerComparisonCard player={selectedB} />
              </div>
            )}
          </section>
        </main>
      )}
    </div>
  );
}

export default App;