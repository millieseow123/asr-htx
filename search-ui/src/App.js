import "@elastic/react-search-ui-views/lib/styles/styles.css";
import {
  SearchProvider,
  SearchBox,
  Results,
  Paging,
  PagingInfo,
  ResultsPerPage,
  Facet,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import { CustomFacetView } from "./components/customFacet";
import "./App.css"

const customConnector = {
  onSearch: async (state) => {
    const filters = state.filters.reduce((acc, filter) => {
      acc[filter.field] = filter.values[0];
      return acc;
    }, {});

    const params = new URLSearchParams({
      generated_text: state.searchTerm || "",
      resultsPerPage: state.resultsPerPage?.toString() || "10",
      ...filters,
    });


    const res = await fetch(`http://localhost:8002/search?${params}`);
    const json = await res.json();

    return {
      results: json.results.map((doc, index) => ({
        id: { raw: doc._id || index },
        ...Object.fromEntries(
          Object.entries(doc._source).map(([k, v]) => [k, { raw: v }])
        )
      })),
      totalResults: json.results.length,
      facets: json.facets
    };
  },
};

const config = {
  apiConnector: customConnector,
  trackUrlState: false,
  searchQuery: {
    resultsPerPage: 10,
    search_fields: {
      text: {},
      generated_text: {},
      duration: {},
      age: {},
      gender: {},
      accent: {}
    },
    result_fields: {
      filename: { raw: {} },
      text: { raw: {} },
      generated_text: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} },
      duration: { raw: {} }
    },
    disjunctiveFacets: ["age", "gender", "accent", "duration"],
    facets: {
      age: { type: "value", size: 9 },
      gender: { type: "value", size: 3 },
      accent: { type: "value", size: 16 },
      duration: {
        type: "range",
        ranges: [
          { from: 0, to: 2, name: "Very short (0–2s)" },
          { from: 2, to: 4, name: "Short (2–4s)" },
          { from: 4, to: 6, name: "Medium (4–6s)" },
          { from: 6, to: 8, name: "Long (6–8s)" },
          { from: 8, name: "Very long (8s+)" }
        ]
      },
      show: true
    }
  }
};


export default function Search() {

  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => (
          <div className="App" style={{ fontFamily: "Arial", padding: "2rem" }}>
            <Layout
              header={<SearchBox inputProps={{ placeholder: "Search transcript text" }} searchAsYouType={true} />}
              sideContent={
                <div className="sui-side-content">
                  <Facet field="age" label="Age" filterType="any" view={CustomFacetView} />
                  <Facet field="gender" label="Gender" filterType="any" view={CustomFacetView} />
                  <Facet field="accent" label="Accent" filterType="any" view={CustomFacetView} />
                  <Facet field="duration" label="Duration" />
                </div>
              }
              bodyHeader={<>
                {wasSearched && <PagingInfo />}
                {wasSearched && <ResultsPerPage options={[10, 20, 50, 100, 500]} />}
              </>}
              bodyContent={
                <>
                  {!wasSearched && (
                    <div className="info-message">
                      <p>Start typing to see results</p>
                    </div>
                  )}
                  <Results
                    resultView={({ result }) => {
                      const rawFilename = result.filename?.raw || "";
                      const displayedFilename = rawFilename.replace("cv-valid-dev/", "");

                      const transcript = result.generated_text?.raw || "No transcript";
                      const actual = result.text?.raw || "No text";

                      const age = result.age?.raw || "-";
                      const gender = result.gender?.raw || "-";
                      const accent = result.accent?.raw || "-";

                      const duration = result.duration?.raw
                        ? parseFloat(result.duration.raw).toFixed(3) + "s"
                        : "-";

                      return (
                        <div style={{ marginBottom: "1rem" }}>
                          <strong>{displayedFilename}</strong>
                          <p><strong>Transcribed: </strong>
                            <em>{transcript}</em>
                          </p>
                          <p><strong>Actual: </strong>
                            {actual.charAt(0).toUpperCase() + actual.slice(1)}
                          </p>

                          {/* <p><em>{transcript}</em></p> */}
                          <small>
                            Age: {age} | Gender: {gender} | Accent: {accent} | Duration: {duration}
                          </small>
                        </div>
                      );
                    }}
                  />
                </>
              }
              bodyFooter={<Paging />}
            />
          </div>
        )}
      </WithSearch>
    </SearchProvider>
  );
}
