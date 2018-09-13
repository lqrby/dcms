import math

class VectorCompare():
    # 计算矢量大小
    # 计算平方和
    def magnitude(self, concordance):
        total = 0
        # concordance.iteritems:报错'dict' object has no attribute 'iteritems'
        # concordance.items()
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    # 计算矢量之间的 cos 值
    def relation(self, concordance1, concordance2):
        topvalue = 0
        # concordance1.iteritems:报错'dict' object has no attribute 'iteritems'
        # concordance1.items()
        for word, count in concordance1.items():
            # if concordance2.has_key(word):报错'dict' object has no attribute 'has_key'
            # 改成word in concordance2
            if word in concordance2:
                # 计算相乘的和
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
    