input_layer_g_1 = Input(shape=(29,1), dtype='float32')
input_layer_g_2 = Input(shape=(29,1), dtype='float32')

second_layer_g = Dense(20, activation='relu')(input_layer_g_1)
third_layer_g=Dense(20, activation='relu')(second_layer_g)


combine_layer = merge([third_layer_g,input_layer_g_2], mode='concat')
combine_layer=combine_layer.Flat
output_layer1 = Dense(1, activation='relu')(combine_layer)

general_model = Model(inputs=[input_layer_g_1,input_layer_g_2], outputs=output_layer1)
general_model.compile(loss='mae', optimizer='adam', )

general_model.summary()
