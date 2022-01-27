from rest_framework import serializers

from goods.models import SKU


class CartsSerializer(serializers.Serializer):
    sku_id = serializers.CharField(label='sku_id')
    count = serializers.IntegerField(label='数量', min_value=1)
    is_selected = serializers.BooleanField(label='是否选中', default=True)

    def validate(self, data):
        try:
            sku = SKU.objects.get(id=data['sku_id'])
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        # stock = sku.stock
        # if data['count'] > stock:
        #     raise serializers.ValidationError('库存不足')  # 此处校验库存

        return data


class CartSKUSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(label='数量', min_value=1)
    is_selected = serializers.BooleanField(label='是否选中', default=True)

    class Meta:
        model = SKU
        fields = ('id', 'count', 'name', 'default_image_url', 'price', 'is_selected')