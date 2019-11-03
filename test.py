from pyvi import ViTokenizer, ViPosTagger

b =ViTokenizer.tokenize(u"Trường đại học bách khoa hà nội")

a = ViPosTagger.postagging(ViTokenizer.tokenize(u'''Phần phụ sau thì có các yếu tố bổ sung nghĩa về mặt chất lượng và tăng
dần tính cụ thể hoá đối với phần trung tâm.
Phần trung tâm của danh ngữ thường là một danh từ hoặc một ngữ danh
từ đảm nhận. Trong đó ngữ danh từ gồm một danh từ chỉ loại đứng trước
và một danh từ chỉ sự vật hay một động từ, tính từ chỉ hoạt động, trạng
thái, tính chất… '''))

print (a)



# - A - Adjective
# - C - Coordinating conjunction
# - E - Preposition
# - I - Interjection
# - L - Determiner
# - M - Numeral
# - N - Common noun
# - Nc - Noun Classifier
# - Ny - Noun abbreviation
# - Np - Proper noun
# - Nu - Unit noun
# - P - Pronoun
# - R - Adverb
# - S -  Subordinating conjunction
# - T - Auxiliary, modal words
# - V - Verb
# - X - Unknown
# - F - Filtered out (punctuation)

