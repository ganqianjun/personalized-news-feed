# -*- coding: utf-8 -*

from sklearn.feature_extraction.text import TfidfVectorizer

news1 = """
A US and Japanese missile test conducted in Hawaii missed its target, but both militaries stopped short of calling it a failure.

The firing involved a SM-3 Block IIA missile that's built for the Aegis Missile Defense system, which is used to shoot down medium- and intermediate-range ballistic missiles from ships at sea.
The missile was fired Wednesday evening local time.
The SM-3 Block IIA is not currently in use by either Japan or the United States, according to the US Missile Defense Agency.

This was the missile's second intercept test. The first, which took place in February, was a success.
The Aegis system is designed to intercept a ballistic missile around the middle of its flight, when the missile is at its highest point above the Earth.
It operates similar to the Terminal High Altitude Area Defense system (THAAD) system that's been partially deployed in South Korea.
Both THAAD and Aegis are key pillars of the American strategy to contain the threat from North Korea. The United States has invested billions of dollars in these systems in the hope that they would be able to shoot down North Korean ballistic missiles in the event of a conflict.

Aegis is based on the powerful AN/SPY-1 radar, which can track 100 missiles simultaneously.
China sees these missile defense systems as destabilizing in the region, especially THAAD, and is strongly opposed to its deployment.
Analysts say Beijing worries the radars could be used to monitor activity inside China.
The US Navy has 22 guided-missile cruisers and 62 guided-missile destroyers equipped with the Aegis system. Japan has six Aegis destroyers with plans for more. South Korea also operates Aegis-equipped destroyers.
"""

news2 = """
A joint missile defense test conducted by the U.S. and Japan failed to intercept a targeted rocket over the Pacific on Wednesday, the U.S. Missile Defense Agency (MDA) said.

The failed attempt was the second intercept test of the Standard Missile-3 (SM-3) Block IIA missile, which is being developed by the U.S. and Japan to intercept medium- and intermediate-range ballistic rockets. The first test in February was successful.

Wednesday's test included the launch of a medium-range ballistic missile from a base in Hawaii at 7:20 p.m. local time, the MDA said in a release. The USS John Paul Jones, a guided-missile destroyer outfitted with the Aegis weapon system, tracked the missile, launching an SM-3 Block IIA guided missile to intercept the target.

However, the intercept "was not achieved," the MDA said, providing no further details.

"Program officials will conduct an extensive analysis of the test data" and release additional information following a review, the agency said.

The Japanese Ministry of Defense participated in Wednesday's test. Japan is a key U.S. and South Korean ally, and U.S. missile defense programs utilize radar systems based in the country.

The test comes as the U.S. seeks to counter the threat from North Korea's missile program amid rising tensions in the region. The North Korean regime has conducted multiple missile tests in recent months, including a May 14 test of a medium-range rocket that was its most successful to date. U.S. intelligence believes the country is intent on developing an intercontinental ballistic missile (ICBM) capable of reaching U.S. soil.

In May, the U.S. successfully shot down a target resembling an ICBM in a test for the first time. That test featured a missile launched from the California coast intercepting a rocket outfitted with a mock warhead over the Pacific, in what the MDA called "an incredible accomplishment."

In an interview with "CBS This Morning" co-host Norah O'Donnell, recently elected South Korean President Moon Jae-in called North Korea's missile program "a matter of life and death."

"I believe when it comes to North Korea's nuclear missile threats, it is the Republic of Korea that is more dire," Moon said. "For the United States the North Korean threat is a future threat on the horizon. But for us this is a matter of life and death."

"""

documents = [news1, news2]

tfidf = TfidfVectorizer().fit_transform(documents)
pairwise_sim = tfidf * tfidf.T

print pairwise_sim.A
