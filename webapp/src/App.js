import React, { Component } from 'react'
import extend from 'lodash/extend'
import { SearchkitManager,SearchkitProvider,
  SearchBox, RefinementListFilter, Pagination,
  HierarchicalMenuFilter, HitsStats, SortingSelector, NoHits,
  ResetFilters, RangeFilter, NumericRefinementListFilter,
  ViewSwitcherHits, ViewSwitcherToggle, DynamicRangeFilter,
  InputFilter, GroupedSelectedFilters,
  Layout, TopBar, LayoutBody, LayoutResults,
  ActionBar, ActionBarRow, SideBar,
  TermQuery, FilteredQuery, BoolShould } from 'searchkit'
import './index.css'

const host = "http://localhost:9200/libsearch"
const searchkit = new SearchkitManager(host)

// searchkit.addDefaultQuery((query)=> {
//   return query.addQuery(SimpleQueryString({
//     filter:BoolShould([
//       TermQuery("colour", "red"),
//       TermQuery("colour", "orange")
//     ])
//   }))})

const MovieHitsGridItem = (props)=> {
  const {bemBlocks, result} = props
  let url = "http://www.imdb.com/title/" + result._source.asset
  const source = extend({}, result._source, result.highlight)
  return (
    <div className={bemBlocks.item().mix(bemBlocks.container("item"))} data-qa="hit">
      <a href={url} target="_blank">
        {result._source.asset}
        {/* <img data-qa="apk" alt="presentation" className={bemBlocks.item("poster")} src={result._source.poster} width="170" height="240"/> */}
        {/* <div data-qa="title" className={bemBlocks.item("title")} dangerouslySetInnerHTML={{__html:source.title}}></div> */}
      </a>
    </div>
  )
}

const MovieHitsListItem = (props)=> {
  const {bemBlocks, result} = props
  let url = "http://www.imdb.com/title/" + result._source.asset
  const source = extend({}, result._source, result.highlight)
  return (
    <div><a href={url} target="_blank">{result._source.data}</a></div>
    // <div className={bemBlocks.item().mix(bemBlocks.container("item"))} data-qa="hit">
    //   <div className={bemBlocks.item("poster")}>
    //     <img alt="presentation" data-qa="poster" src={result._source.poster}/>
    //   </div>
    //   <div className={bemBlocks.item("details")}>
    //     <a href={url} target="_blank"><h2 className={bemBlocks.item("title")} dangerouslySetInnerHTML={{__html:source.title}}></h2></a>
    //     <h3 className={bemBlocks.item("subtitle")}>Released in {source.year}, rated {source.imdbRating}/10</h3>
    //     <div className={bemBlocks.item("text")} dangerouslySetInnerHTML={{__html:source.plot}}></div>
    //   </div>
    // </div>
  )
}

class App extends Component {
  render() {
    return (
      <SearchkitProvider searchkit={searchkit}>
        <Layout>
          <TopBar>
            <div className="my-logo">Searchkit Acme co</div>
            {/* ,"type^2","languages","title^10" */}
            <SearchBox autofocus={true} searchOnChange={true} queryFields={["data"]} />
          </TopBar>

        <LayoutBody>

          <SideBar>
          
          <RefinementListFilter id="type" title="Type" field="dtype.keyword" size={10}/>
          <RefinementListFilter id="apk" title="APK" field="asset.keyword"/>
          
            {/* <HierarchicalMenuFilter fields={["type.raw", "genres.raw"]} title="Categories" id="categories"/>
            <DynamicRangeFilter field="metaScore" id="metascore" title="Metascore" rangeFormatter={(count)=> count + "*"}/>
            <RangeFilter min={0} max={10} field="imdbRating" id="imdbRating" title="IMDB Rating" showHistogram={true}/>
            <InputFilter id="writers" searchThrottleTime={500} title="Writers" placeholder="Search writers" searchOnChange={true} queryFields={["writers"]} />
            
            <RefinementListFilter id="writersFacets" translations={{"facets.view_more":"View more writers"}} title="Writers" field="writers.raw" operator="OR" size={10}/>
            <RefinementListFilter id="countries" title="Countries" field="countries.raw" operator="OR" size={10}/>
            <NumericRefinementListFilter id="runtimeMinutes" title="Length" field="runtimeMinutes" options={[
              {title:"All"},
              {title:"up to 20", from:0, to:20},
              {title:"21 to 60", from:21, to:60},
              {title:"60 or more", from:61, to:1000}
            ]}/> */}
          </SideBar>
          <LayoutResults>
            <ActionBar>

              <ActionBarRow>
                <HitsStats translations={{
                  "hitstats.results_found":"{hitCount} results found"
                }}/>
                <ViewSwitcherToggle/>
                <SortingSelector options={[
                  {label:"Relevance", field:"_score", order:"desc"},
                  {label:"Latest Releases", field:"released", order:"desc"},
                  {label:"Earliest Releases", field:"released", order:"asc"}
                ]}/>
              </ActionBarRow>

              <ActionBarRow>
                <GroupedSelectedFilters/>
                <ResetFilters/>
              </ActionBarRow>

            </ActionBar>
            <ViewSwitcherHits
                hitsPerPage={12} //highlightFields={["title","plot"]}
                sourceFilter={["data"]}
                hitComponents={[
                  {key:"grid", title:"Grid", itemComponent:MovieHitsGridItem, defaultOption:true},
                  {key:"list", title:"List", itemComponent:MovieHitsListItem}
                ]}
                scrollTo="body"
            />
            <NoHits />
            <Pagination showNumbers={true}/>
          </LayoutResults>

          </LayoutBody>
        </Layout>
      </SearchkitProvider>
    );
  }
}

export default App;
