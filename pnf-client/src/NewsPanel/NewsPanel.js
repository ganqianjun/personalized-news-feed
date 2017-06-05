import './NewsPanel.css';
import React from 'react';

import NewsCard from '../NewsCard/NewsCard';

class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = {
      news: null
    };
  }

  componentDidMount() {
    this.loadMoreNews();
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

  // Iterate each news in state.news and create NewsCard for it
  renderNews() {
    const news_list = this.state.news.map(function(news) {
      return (
        <a className="list-group-item" key={news.digest} href='#'>
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
