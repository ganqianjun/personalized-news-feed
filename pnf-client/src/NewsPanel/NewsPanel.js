import './NewsPanel.css';
import React from 'react';
import _ from 'lodash';

import NewsCard from '../NewsCard/NewsCard';

class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = {
      news: null
    };
    this.handleScroll = this.handleScroll.bind(this);
  }

  componentDidMount() {
    this.loadMoreNews();
    // to retrieve from server only once every 1s
    this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
    window.addEventListener('scroll', this.handleScroll);
  }

  // Load news from backend, currently only 2 sample news
  loadMoreNews() {
    let request = new Request('http://localhost:3000/news', {
      method: 'GET',
      cache: false // make sure f5 is a real f5
    });

    // return a promise
    fetch(request)
      .then((res) =>  res.json()) // transfer to JSON
      .then((loadedNews) => {
        // the previous news is empty, then use 'loadedNews'
        // or we need to add 'loadedNews' after previous news
        this.setState({
          news: this.state.news ? this.state.news.concat(loadedNews) : loadedNews
        });
      });
  }

  handleScroll() {
    // window.scrollY : current page that scrolls to (pixel in Y)
    // window.pageYOffset is the old version of window.scrollY
    // document.documentElement.scrollTop - for IE
    let scrollY = window.scrollY ||
                  window.pageYOffset ||
                  document.documentElement.scrollTop;
    // window.innerHeight is the visual window height
    // window.innerHeight + scrollY  - the height of the whole page
    if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
      console.log('App.js : Loading more news...');
      this.loadMoreNews();
    }
  }

  // Iterate each news in state.news and create NewsCard for it
  renderNews() {
    const news_list = this.state.news.map(function(news) {
      // return (
      //   <a className="list-group-item" key={news.digest} href='#'>
      //     <NewsCard news={news} />
      //   </a>
      // );
      return (
        <a className="list-group-item" href='#'>
          <NewsCard news={news} />
        </a>
      );
    });

    return (
      <div className="container-fluid">
        <div className="list-group">
          {news_list}
        </div>
      </div>
    )
  }

  render() {
    if (this.state.news) {
      return (
        <div> '{this.renderNews()}' </div>
      );
    }
    else {
      return (
        <div> Loading... </div>
      );
    }
  }
}

export default NewsPanel;
