import re
import pytest
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from collections import Counter, defaultdict


class Movies:
    """
    Analyzing data from movies.csv
    """
    def __load_data(self):
        try:
            with open(self.path_to_the_file, 'r', encoding='utf-8') as file:
                headers = file.readline().strip().split(',')
                if headers != ['movieId', 'title', 'genres']:
                    raise Exception("Titles should be: 'movieId', 'title', 'genres'")
                for line in file.read().split('\n'):
                    parse_line = self.__parse_line(line)
                    if parse_line is not None:
                        data = dict(zip(headers, parse_line))
                        data['movieId'] = int(data['movieId'])
                        data['genres'] = data['genres'].split('|')
                        
                        re_year = re.search(r'\(\d{4}\)', data['title'])
                        if re_year is not None:
                            data['year'] = int(re_year.group(0)[1:-1])
                            data['title'] = data['title'].replace(f'({data['year']})', '').strip()
                        self.data.append(data)
                self.movie_dict = {movie['movieId']: movie for movie in self.data}
        except FileNotFoundError:
            print(f"File not found: {self.path_to_the_file}")
        except Exception as e:
            print(f"Error loading data: {e}")
                
    def __parse_line(self, line):
        fields = []
        current_field = ''
        in_quotes = False
        
        for ch in line:
            if ch == '"':
                in_quotes = not in_quotes
            elif ch == ',' and not in_quotes:
                fields.append(current_field.strip('"'))
                current_field = ''
            else:
                current_field += ch
        fields.append(current_field.strip('"'))
        
        if len(fields) != 3:
            return None
        return fields
        
    def __init__(self, path_to_the_file):
        self.data = []
        self.movie_dict = dict()
        self.path_to_the_file = path_to_the_file
        self.__load_data()
    
    def __len__(self):
        return len(self.data)
        
    def get_title_by_id(self, movie_id):
        if not isinstance(movie_id, int):
            raise TypeError('Expected "movie_id" as integer')
        if movie_id <= 0:
            raise ValueError('Expected "movie_id" as positive integer')
            
        if movie_id not in self.movie_dict.keys():
            return None
        return self.movie_dict[movie_id]['title']
            
    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        years = [movie['year'] for movie in self.data if 'year' in movie]
        release_years = dict(sorted(Counter(years).items(), key=lambda x: x[1], reverse=True))
        
        return release_years
    
    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """
        list_of_genres = []
        
        for movie in self.data:
            list_of_genres += movie['genres']
        
        genres = dict(sorted(Counter(list_of_genres).items(), key=lambda x: x[1], reverse=True))
        return genres
        
    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        if not isinstance(n, int):
            raise TypeError('Expected "n" as integer')
        if n <= 0:
            raise ValueError('Expected "n" as positive integer')
        
        movies = defaultdict(int)
        for movie in self.data:
            movies[movie['title']] += len(movie['genres'])
        movies = dict(sorted(movies.items(), key=lambda x: x[1], reverse=True)[:n])

        return movies


class Ratings:
    """
    Analyzing data from ratings.csv
    """
    
    def __len__(self):
        return len(self.data)

    def __init__(self, path_to_the_file, movies_ref):
        """
        Put here any fields that you think you will need.
        """
        self.data = []
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as file:
                headers = file.readline().strip().split(',') + ['title']
                if headers != ['userId', 'movieId', 'rating', 'timestamp', 'title']:
                    raise Exception("Titles should be: 'userId', 'movieId', 'rating', 'timestamp")
                for line in file:
                    values = [int(value) if i != 2 else float(value) for i, value in enumerate(line.strip().split(','))]
                    movie_id = values[1]
                    title = movies_ref.get_title_by_id(movie_id)
                    values.append(title)
                    dict_values = dict(zip(headers, values))
                    self.data.append(dict_values)
        except FileNotFoundError:
            print(f"File not found: {path_to_the_file}")
        except Exception as e:
            print(f"Error loading data: {e}")

    class Movies:
        def __init__(self, path_to_the_file, movies_ref=None):
            Ratings.__init__(self, path_to_the_file, movies_ref)
            self._id = "movieId"

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            data = defaultdict(int)
            for d in self.data:
                year = datetime.fromtimestamp(d['timestamp']).year
                data[year] += 1
            return dict(sorted(data.items(), key=lambda year: year[0]))

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            data = defaultdict(int)
            for d in self.data:
                rating = d['rating']
                data[rating] += 1
            return dict(sorted(data.items(), key=lambda rating: rating[0]))

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            if not isinstance(n, int):
                raise TypeError("Expected n as integer")
            if n <= 0:
                raise ValueError("Expected n as positive integer")
            data = defaultdict(int)
            for d in self.data:
                id = d['title'] if self._id == 'movieId' else d[self._id]
                data[id] += 1
            sorted_by_rating = sorted(data.items(), key=lambda rating: rating[1], reverse=True)
            top_n = dict(sorted_by_rating[:n])
            return top_n

        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            if not isinstance(n, int):
                raise TypeError("Expected n as integer")
            if n <= 0:
                raise ValueError("Expected n as positive integer")
            if not isinstance(metric, str):
                raise TypeError("Expected metric as string")
            
            data = defaultdict(list)
            for d in self.data:
                id = d['title'] if self._id == 'movieId' else d[self._id]
                rating = d['rating']
                data[id].append(rating)

            if metric == 'average':
                data = {id: round(sum(ratings) / len(ratings), 2) for id, ratings in data.items()}
            elif metric == 'median':
                for id in data:
                    sorted_rating = sorted(data[id])
                    mid = len(sorted_rating) // 2
                    if len(sorted_rating) % 2 == 0:
                        median = (sorted_rating[mid-1] + sorted_rating[mid]) / 2
                    else:
                        median = sorted_rating[mid]
                    data[id] = round(median, 2)
            else:
                raise ValueError("Expected metric as 'average' or 'median'")
            
            sorted_by_ratings = sorted(data.items(), key=lambda rating: rating[1], reverse=True)
            top_n = dict(sorted_by_ratings[:n])
            return top_n

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            if not isinstance(n, int):
                raise TypeError("Expected n as integer")
            if n <= 0:
                raise ValueError("Expected n as positive integer")
            
            data = defaultdict(list)
            for d in self.data:
                id = d['title'] if self._id == 'movieId' else d[self._id]
                rating = d['rating']
                data[id].append(rating)

            for id, ratings in data.items():
                average = sum(ratings) / len(ratings)
                deviations = [(rating - average) ** 2 for rating in ratings]
                variance = sum(deviations) / len(deviations)
                data[id] = round(variance, 2)

            sorted_by_rating = sorted(data.items(), key=lambda rating: rating[1], reverse=True)
            top_n = dict(sorted_by_rating[:n])
            return top_n

    class Users(Movies):
        """
        In this class, three methods should work. 
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """
        def __init__(self, path_to_the_file, movies_ref=None):
            super().__init__(path_to_the_file, movies_ref)
            self._id = "userId"

        def top_by_num_of_ratings(self, n):
            return super().top_by_num_of_ratings(n)
        
        def top_by_ratings(self, n, metric='average'):
            return super().top_by_ratings(n, metric)
        
        def top_controversial(self, n):
            return super().top_controversial(n)


class Tags:
    """
    Analyzing data from tags.csv
    """
    def __len__(self):
        return len(self.tags_list)
    
    def __load_data(self):
        tags_list = []
        try:
            with open(self.path_to_the_file, 'r', encoding='utf-8') as file:
                headers = file.readline().strip().split(',')
                if headers != ['userId', 'movieId', 'tag', 'timestamp']:
                    raise Exception("Titles should be: 'userId', 'movieId', 'tag', 'timestamp'")
                for line in file:
                    tag = line.strip().split(',')[2]
                    tags_list.append(tag)
        except FileNotFoundError:
            print(f"Файл не найден: {self.path_to_the_file}")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
        self.tags_list = tags_list

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path_to_the_file = path_to_the_file
        self.__load_data()

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        unique_list = list(set(self.tags_list))
        top_words_dict = {}
        try:
            tag_word_count = {tag: len(tag.split()) for tag in unique_list}
            top_words_dict = dict(sorted(tag_word_count.items(), key=lambda x: x[1], reverse=True)[:n])
        except Exception as e:
            print(f"Ошибка при создании словаря тэгов")
        return top_words_dict

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        unique_list = list(set(self.tags_list))
        top_chars_list = []
        try:
            tags_chars_dict = {tag: len(tag) for tag in unique_list}
            top_chars_list = [tag for tag, _ in sorted(tags_chars_dict.items(),
                                                 key=lambda x: x[1],
                                                 reverse=True)[:n]]
        except Exception as e:
            print(f"Ошибка при определении самых длинных тэгов")
        return top_chars_list

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        Суть метода в том, что он сначала формирует два списка (самые "многословные" теги и самые "длинные" теги),
        а затем находит теги, которые есть в обоих списках. Это и есть пересечение.
        """
        top_chars_list = self.longest(n)
        top_words_dict = self.most_words(n)
        top_words_list = list(top_words_dict.keys())
        common_tags = []
        try:
            common_tags = set(top_words_list) & set(top_chars_list)
        except Exception as e:
            print(f"Ошибка при поиске пересечений в тэгах")
        return common_tags
        
    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        popular_tags = {}
        try:
            popular_tags = dict(sorted(Counter(self.tags_list).items(), key=lambda x: x[1], reverse=True)[:n])
        except Exception as e:
            print(f"Ошибка при поиске самых популярных тэгов")
        return popular_tags
        
    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        tags_with_word = []
        try:
            tags_with_word = set([tag for tag in self.tags_list if word.lower() in tag.lower()])
        except Exception as e:
            print(f"Ошибка при поиске тэгов со словом {word}")
        return tags_with_word


class Links:
    def __len__(self):
        return len(self.data)
    
    def __get_fields_on_imdb(self, imdb_id, fields):
        headers = {
            "accept": "text/html",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.132 Safari/537.36"
        }
        response = requests.get(f'http://www.imdb.com/title/tt{imdb_id}/', headers=headers)
        if response.status_code != 200:
            raise ConnectionError("Failed to fetch IMDb page")
        soup = BeautifulSoup(response.text, "html.parser")
        text = []
        for field in fields:
            element = soup.find('span', string=field)
            next_element = element.find_next_sibling('div') if element else None
            text.append(next_element.text if next_element else None)
        return text
    
    def __get_currrency(self, currency_str):
        currency = re.search(r'.([0-9,]+)', currency_str).group(1)
        currency = currency.split(",")
        return int("".join(currency))
    
    def __get_runtime(self, runtime_str):
        return int(re.search(r'\(([0-9]+) min\)', runtime_str).group(1))
    
    def __init__(self, path_to_the_file, movies_ref):
        self.data = []
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as file:
                headers = file.readline().strip().split(',') + ['title']
                if headers != ['movieId', 'imdbId', 'tmdbId', 'title']:
                    raise Exception("Titles should be: 'movieId', 'imdbId', 'tmdbId'")
                for line in file:
                    fields = line.strip().split(',')
                    fields[0] = int(fields[0])
                    movie_id = fields[0]
                    title = movies_ref.get_title_by_id(movie_id)
                    fields.append(title)
                    dict_data = dict(zip(headers, fields))
                    self.data.append(dict_data)
        except FileNotFoundError:
            print(f"File not found: {path_to_the_file}")
        except Exception as e:
            print(f"Error loading data: {e}")
        self.data = self.data[:10] # для теста, иначе очень много запросов
        self.movie = movies_ref

    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        if not isinstance(list_of_movies, list):
            raise TypeError("Expected list_of_movies as list")
        if not isinstance(list_of_fields, list):
            raise TypeError("Expected list_of_fields as list")
        
        imdb_info = []
        sorted_list_of_movies = sorted(list_of_movies, key=lambda movie_id: movie_id, reverse=True)
        for movie_id in sorted_list_of_movies:
            imdb_id = None
            for d in self.data:
                if d['movieId'] == movie_id:
                    imdb_id = d['imdbId']
                    break
            if not imdb_id:
                continue
            fields = self.__get_fields_on_imdb(imdb_id, list_of_fields)
            imdb_info.append([movie_id] + fields)
        return imdb_info
        
    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        if not isinstance(n, int):
            raise TypeError("Expected n as integer")
        if n <= 0:
            raise ValueError("Expected n as positive integer")
        
        directors = defaultdict(int)
        for d in self.data:
            imdb_id = d['imdbId']
            director = self.__get_fields_on_imdb(imdb_id, ["Director"])[0]
            if director:
                directors[director] += 1
        sorted_directors = sorted(directors.items(), key=lambda numbers: numbers[1], reverse=True)
        return dict(sorted_directors[:n])
        
    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        if not isinstance(n, int):
            raise TypeError("Expected n as integer")
        if n <= 0:
            raise ValueError("Expected n as positive integer")
        
        budgets_of_movies = dict()
        for d in self.data:
            title = d['title']
            imdb_id = d['imdbId']
            budget = self.__get_fields_on_imdb(imdb_id, ["Budget"])[0]
            if budget:
                budgets_of_movies[title] = self.__get_currrency(budget)
        sorted_by_budget = sorted(budgets_of_movies.items(), key=lambda budget: budget[1], reverse=True)
        return dict(sorted_by_budget[:n])

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        if not isinstance(n, int):
            raise TypeError("Expected n as integer")
        if n <= 0:
            raise ValueError("Expected n as positive integer")
        
        profits = defaultdict(int)
        for d in self.data:
            title = d['title']
            imdb_id = d['imdbId']
            gross, budget = self.__get_fields_on_imdb(imdb_id, ["Gross worldwide", "Budget"])
            gross = self.__get_currrency(gross) if gross else None
            budget = self.__get_currrency(budget) if budget else None
            if gross and budget:
                profits[title] = gross - budget
        sorted_by_profit = sorted(profits.items(), key=lambda profit: profit[1], reverse=True)
        return dict(sorted_by_profit[:n])

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version - choose any.
        Sort it by runtime descendingly.
        """
        if not isinstance(n, int):
            raise TypeError("Expected n as integer")
        if n <= 0:
            raise ValueError("Expected n as positive integer")
        
        runtimes = dict()
        for d in self.data:
            title = d['title']
            imdb_id = d['imdbId']
            runtime = self.__get_fields_on_imdb(imdb_id, ['Runtime'])[0]
            minutes = self.__get_runtime(runtime)
            if minutes:
                runtimes[title] = minutes
        sorted_runtimes = sorted(runtimes.items(), key=lambda runtime: runtime[1], reverse=True)
        return dict(sorted_runtimes[:n])

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies - do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        if not isinstance(n, int):
            raise TypeError("Expected n as integer")
        if n <= 0:
            raise ValueError("Expected n as positive integer")
        
        costs = dict()
        for d in self.data:
            title = d['title']
            imdb_id = d['imdbId']
            budget, runtime = self.__get_fields_on_imdb(imdb_id, ['Budget', 'Runtime'])
            budget = self.__get_currrency(budget) if budget is not None else None
            minutes = self.__get_runtime(runtime) if runtime is not None else None
            if budget and minutes:
                cost = budget / minutes
                costs[title] = round(cost, 2)
        sorted_costs = sorted(costs.items(), key=lambda cost: cost[1], reverse=True)
        return dict(sorted_costs[:n])
            

class Tests:
    class TestMovies:
        def test_get_title_by_id(self):
            movies = Movies('movies.csv')
            result = movies.get_title_by_id(1)
            assert isinstance(result, (str, type(None)))
            
            with pytest.raises(TypeError, match='Expected "movie_id" as integer'):
                movies.get_title_by_id("meow")
            with pytest.raises(ValueError, match='Expected "movie_id" as positive integer'):
                movies.get_title_by_id(-1)
                
        def test_dist_by_release(self):
            movies = Movies('movies.csv')
            result = movies.dist_by_release()
            
            assert isinstance(result, dict)
            assert all(map(lambda x: re.fullmatch(r'\d{4}', str(x)), result.keys()))
            assert all(map(lambda x: isinstance(x, int), result.values()))
            assert list(result.values()) == sorted(list(result.values()), reverse=True)
            
        def test_dist_by_genres(self):
            movies = Movies('movies.csv')
            result = movies.dist_by_genres()
            
            assert isinstance(result, dict)
            assert all(map(lambda x: isinstance(x, str), result.keys()))
            assert all(map(lambda x: isinstance(x, int), result.values()))
            assert list(result.values()) == sorted(list(result.values()), reverse=True)     

        def test_most_genres(self):
            movies = Movies('movies.csv')
            result = movies.most_genres(10)
            
            assert isinstance(result, dict)
            assert all(map(lambda x: isinstance(x, str), result.keys()))
            assert all(map(lambda x: isinstance(x, int), result.values()))
            assert list(result.values()) == sorted(list(result.values()), reverse=True)
            
            with pytest.raises(TypeError, match='Expected "n" as integer'):
                movies.most_genres("meow")
            with pytest.raises(ValueError, match='Expected "n" as positive integer'):
                movies.most_genres(-1)
                
    class TestRatings:
        class TestMovies:
            def __ratings_movies(self):
                movies = Movies("movies.csv")
                ratings_movies = Ratings.Movies("ratings.csv", movies)
                return ratings_movies
            
            def test_ratings_movies_dist_by_year(self):
                result = self.__ratings_movies().dist_by_year()
                # type data
                assert isinstance(result, dict)
                # type elements
                for year, counts in result.items():
                    assert isinstance(year, int)
                    assert isinstance(counts, int)
                # sorted correctly
                years = list(result.keys())
                for i in range(len(years) - 1):
                    assert years[i] <= years[i + 1]

            def test_ratings_movies_dist_by_rating(self):
                result = self.__ratings_movies().dist_by_rating()
                # type data
                assert isinstance(result, dict)
                # type elements
                for rating, counts in result.items():
                    assert isinstance(rating, float)
                    assert isinstance(counts, int)
                # sorted correctly
                ratings = list(result.keys())
                for i in range(len(ratings) - 1):
                    assert ratings[i] <= ratings[i + 1]
                
            def test_ratings_movies_top_by_num_of_ratings(self):
                ratings_movies = self.__ratings_movies()
                result = ratings_movies.top_by_num_of_ratings(5)
                # type data
                assert isinstance(result, dict)
                # type elements
                for title, numbers in result.items():
                    assert isinstance(title, str)
                    assert isinstance(numbers, int)
                # sorted correctly
                numbers = list(result.values())
                for i in range(len(numbers) - 1):
                    assert numbers[i] >= numbers[i + 1]
                # correctly length
                assert len(result) == 5
                # invalid argument
                with pytest.raises(TypeError, match="Expected n as integer"):
                    ratings_movies.top_by_num_of_ratings("meow")
                with pytest.raises(ValueError, match="Expected n as positive integer"):
                    ratings_movies.top_by_num_of_ratings(-1)

            def test_ratings_movies_top_by_ratings(self):
                ratings_movies = self.__ratings_movies()
                result = ratings_movies.top_by_ratings(5)
                # type data
                assert isinstance(result, dict)
                # type elements
                for title, metric in result.items():
                    assert isinstance(title, str)
                    assert isinstance(metric, float)
                # sorted correctly
                metrics = list(result.values())
                for i in range(len(metrics) - 1):
                    assert metrics[i] >= metrics[i + 1]
                # correctly length
                assert len(result) == 5
                # invalid arguments
                with pytest.raises(TypeError, match="Expected n as integer"):
                    ratings_movies.top_by_ratings("meow")
                with pytest.raises(ValueError, match="Expected n as positive integer"):
                    ratings_movies.top_by_ratings(-1)
                with pytest.raises(TypeError, match="Expected metric as string"):
                    ratings_movies.top_by_ratings(10, 1)
                with pytest.raises(ValueError, match="Expected metric as 'average' or 'median'"):
                    ratings_movies.top_by_ratings(10, 'meow')

            def test_ratings_movies_top_controversial(self):
                ratings_movies = self.__ratings_movies()
                result = ratings_movies.top_controversial(5)
                # type data
                assert isinstance(result, dict)
                # type elements
                for title, variance in result.items():
                    assert isinstance(title, str)
                    assert isinstance(variance, float)
                # sorted correctly
                variances = list(result.values())
                for i in range(len(variances) - 1):
                    assert variances[i] >= variances[i + 1]
                # correctly length
                assert len(result) == 5
                # invalid argument
                with pytest.raises(TypeError, match="Expected n as integer"):
                    ratings_movies.top_controversial("meow")
                with pytest.raises(ValueError, match="Expected n as positive integer"):
                    ratings_movies.top_controversial(-1)

        class TestUsers:
            def __ratings_users(self):
                movies = Movies("movies.csv")
                ratings_users = Ratings.Users("ratings.csv", movies)
                return ratings_users
            
            def test_ratings_users_top_by_num_of_ratings(self):
                ratings_users = self.__ratings_users()
                result = ratings_users.top_by_num_of_ratings(5)
                # type data
                assert isinstance(result, dict)
                # type elements
                for user, numbers in result.items():
                    assert isinstance(user, int)
                    assert isinstance(numbers, int)
                # sorted correctly
                numbers = list(result.values())
                for i in range(len(numbers) - 1):
                    assert numbers[i] >= numbers[i + 1]
                # correctly length
                assert len(result) == 5
                # invalid argument
                with pytest.raises(TypeError, match="Expected n as integer"):
                    ratings_users.top_by_num_of_ratings("meow")
                with pytest.raises(ValueError, match="Expected n as positive integer"):
                    ratings_users.top_by_num_of_ratings(-1)

            def test_ratings_users_top_by_ratings(self):
                ratings_users = self.__ratings_users()
                result = ratings_users.top_by_ratings(5)
                # type data
                assert isinstance(result, dict)
                # type elements
                for user, metric in result.items():
                    assert isinstance(user, int)
                    assert isinstance(metric, float)
                # sorted correctly
                metrics = list(result.values())
                for i in range(len(metrics) - 1):
                    assert metrics[i] >= metrics[i + 1]
                # correctly length
                assert len(result) == 5
                # invalid arguments
                with pytest.raises(TypeError, match="Expected n as integer"):
                    ratings_users.top_by_ratings("meow")
                with pytest.raises(ValueError, match="Expected n as positive integer"):
                    ratings_users.top_by_ratings(-1)
                with pytest.raises(TypeError, match="Expected metric as string"):
                    ratings_users.top_by_ratings(10, 1)
                with pytest.raises(ValueError, match="Expected metric as 'average' or 'median'"):
                    ratings_users.top_by_ratings(10, 'meow')

            def test_ratings_users_top_controversial(self):
                ratings_users = self.__ratings_users()
                result = ratings_users.top_controversial(5)
                # type data
                assert isinstance(result, dict)
                # type elements
                for user, variance in result.items():
                    assert isinstance(user, int)
                    assert isinstance(variance, float)
                # sorted correctly
                variances = list(result.values())
                for i in range(len(variances) - 1):
                    assert variances[i] >= variances[i + 1]
                # correctly length
                assert len(result) == 5
                # invalid argument
                with pytest.raises(TypeError, match="Expected n as integer"):
                    ratings_users.top_controversial("meow")
                with pytest.raises(ValueError, match="Expected n as positive integer"):
                    ratings_users.top_controversial(-1)

    class TestTags:
        def setUp(self):
            self.Tags = Tags('tags.csv')

        def test_most_words(self):
            self.setUp()
            result = self.Tags.most_words(10)
            assert type(result) == dict, f"Expected dict, got {type(result)}"
            for user, metric in result.items():
                assert isinstance(user, str)
                assert isinstance(metric, int)
            assert sorted(result.items(), key=lambda x: x[1], reverse=True) == list(result.items()), f"Not sorted"

        def test_longest(self):
            self.setUp()
            result = self.Tags.longest(10)
            assert type(result) == list, f"Expected list, got {type(result)}"
            assert sorted(result, key=lambda x: len(x), reverse=True) == result, f"Not sorted"

        def test_most_words_and_longest(self):
            self.setUp()
            result = self.Tags.most_words_and_longest(10)
            assert type(result) == set, f"Expected set, got {type(result)}"
            if len(result) > 0:
                for i in result:
                    assert i in self.Tags.longest(10) and i in list(self.Tags.most_words(10).keys()), f"Unknown tag in set"

        def test_most_popular(self):
            self.setUp()
            result = self.Tags.most_popular(10)
            assert type(result) == dict, f"Expected dict, got {type(result)}"
            for user, metric in result.items():
                assert isinstance(user, str)
                assert isinstance(metric, int)

        def test_tags_with(self):
            self.setUp()
            result = self.Tags.tags_with('mafia')
            assert type(result) == set, f"Expected set, got {type(result)}"
            if len(result) > 0:
                for i in result:
                    assert 'mafia' in i.lower(), f"Unknown word"

    class TestLinks:
        def __links(self):
            movies = Movies("movies.csv")
            links = Links("links.csv", movies)
            return links
        
        def test_links_get_imdb(self):
            links = self.__links()
            result = links.get_imdb([1], ['Cats', 'Budget'])
            # type data
            assert isinstance(result, list)
            # type elements
            for r in result:
                assert isinstance(r, list)
                movie_id, *strings = r
                assert isinstance(movie_id, int)
                for s in strings:
                    assert isinstance(s, str) or s is None
            # sorted correctly
            movies_id = [r[0] for r in result]
            for i in range(len(movies_id) - 1):
                assert movies_id[i] >= movies_id[i + 1]
            # invalid arguments
            with pytest.raises(TypeError, match="Expected list_of_movies as list"):
                links.get_imdb("meow", ['Directors', 'Budget'])
            with pytest.raises(TypeError, match="Expected list_of_fields as list"):
                links.get_imdb([1], "meow")

        def test_links_top_directors(self):
            links = self.__links()
            result = links.top_directors(5)
            # type data
            assert isinstance(result, dict)
            # type elements
            for director, number in result.items():
                assert isinstance(director, str)
                assert isinstance(number, int)
            # sorted correctly
            numbers = list(result.values())
            for i in range(len(numbers) - 1):
                assert numbers[i] >= numbers[i + 1]
            # correct length
            assert len(result) == 5
            # invalid argument
            with pytest.raises(TypeError, match="Expected n as integer"):
                links.top_directors("meow")
            with pytest.raises(ValueError, match="Expected n as positive integer"):
                links.top_directors(-1)

        def test_links_most_expensive(self):
            links = self.__links()
            result = links.most_expensive(5)
            # type data
            assert isinstance(result, dict)
            # type elements
            for title, budget in result.items():
                assert isinstance(title, str)
                assert isinstance(budget, int)
            # sorted correctly
            budgets = list(result.values())
            for i in range(len(budgets) - 1):
                assert budgets[i] >= budgets[i + 1]
            # correct length
            assert len(result) == 5
            # invalid argument
            with pytest.raises(TypeError, match="Expected n as integer"):
                links.most_expensive("meow")
            with pytest.raises(ValueError, match="Expected n as positive integer"):
                links.most_expensive(-1)

        def test_links_most_profitable(self):
            links = self.__links()
            result = links.most_profitable(5)
            # type data
            assert isinstance(result, dict)
            # type elements
            for title, difference in result.items():
                assert isinstance(title, str)
                assert isinstance(difference, int)
            # sorted correctly
            differences = list(result.values())
            for i in range(len(differences) - 1):
                assert differences[i] >= differences[i + 1]
            # correct length
            assert len(result) == 5
            # invalid argument
            with pytest.raises(TypeError, match="Expected n as integer"):
                links.most_profitable("meow")
            with pytest.raises(ValueError, match="Expected n as positive integer"):
                links.most_profitable(-1)

        def test_links_longest(self):
            links = self.__links()
            result = links.longest(5)
            # type data
            assert isinstance(result, dict)
            # type elements
            for title, runtime in result.items():
                assert isinstance(title, str)
                assert isinstance(runtime, int)
            # sorted correctly
            runtimes = list(result.values())
            for i in range(len(runtimes) - 1):
                assert runtimes[i] >= runtimes[i + 1]
            # correct length
            assert len(result) == 5
            # invalid argument
            with pytest.raises(TypeError, match="Expected n as integer"):
                links.longest("meow")
            with pytest.raises(ValueError, match="Expected n as positive integer"):
                links.longest(-1)

        def test_links_top_cost_per_minute(self):
            links = self.__links()
            result = links.top_cost_per_minute(5)
            # type data
            assert isinstance(result, dict)
            # type elements
            for title, cost in result.items():
                assert isinstance(title, str)
                assert isinstance(cost, float)
            # sorted correctly
            costs = list(result.values())
            for i in range(len(costs) - 1):
                assert costs[i] >= costs[i + 1]
            # correct length
            assert len(result) == 5
            # invalid argument
            with pytest.raises(TypeError, match="Expected n as integer"):
                links.top_cost_per_minute("meow")
            with pytest.raises(ValueError, match="Expected n as positive integer"):
                links.top_cost_per_minute(-1)