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
    this.setState({
      news: [
        {
          'url':'http://money.cnn.com/2017/05/31/technology/tujia-airbnb-china-melissa-yang/index.html',
          'title':"China's big Airbnb rival is taking the battle overseasChina's big Airbnb rival is taking the battle overseas",
          'description':"China's leading home-rental site has been a thorn in Airbnb's side in the world's most populous country. China's leading home-rental site has been a thorn in Airbnb's side in the world's most populous country. ",
          'source':'cnn',
          'urlToImage':'http://http://i2.cdn.turner.com/money/dam/assets/170529093311-tujia-airbnb-tech-china-780x439.jpg',
          'digest':'news-01',
          'reason':"Recommended"
        },
        {
          'url':'https://techcrunch.com/2017/06/04/three-computer-vision-experts-join-techcrunchs-tel-aviv-event/',
          'title':"Three computer vision experts join TechCrunch’s Tel Aviv event",
          'description':" Computer vision is a hot topic for the tech industry, and especially in Israel. It seems like Israeli entrepreneurs are one step ahead when it comes to developing computer vision technology.",
          'source':'techcrunch',
          'urlToImage':'https://tctechcrunch2011.files.wordpress.com/2017/02/tel-aviv.jpg?w=738',
          'digest':'news-02',
          'reason':"Hot"
        }
      ]
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
    console.log(this.state.news);
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
