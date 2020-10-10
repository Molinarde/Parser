def get_sqi(driver):
    try:
        sqi = driver.find_element_by_id('auction_sqi').text
    except:
        sqi = ''
    return sqi

def get_name(driver):
    try:
        name = driver.find_element_by_id('field_title').text
    except:
        name = ''
    return name


def get_topic(driver):
    try:
        topic = driver.find_element_by_id('field_type').text
    except:
        topic = ''

    return topic


def get_optimalPrice(driver):
    try:
        optimalPrice = driver.find_element_by_class_name('price_padd').text
        optimalPrice = optimalPrice.replace('&nbsp;', ' ')
        optimalPrice = optimalPrice.replace('&nbsp:', ' ')
    except:
        optimalPrice = ' '
    return optimalPrice

def get_profit(driver):
    try:
        profit = driver.find_element_by_class_name('ok_ico').text
    except:
        profit = ''
    return profit


def get_costs(driver):
    try:
        audience = driver.find_element_by_id('cost').find_element_by_class_name('data-part').text
        audience = audience.replace('&nbsp;', ' ')
        audience = audience.replace('&nbsp:', ' ')
    except:
        audience = ''
    return audience


def get_visit(driver):
    try:
        visit = driver.find_element_by_id('visits_month').text
    except:
        visit = ''
    return visit

def get_views(driver):
    try:
        views = driver.find_element_by_id('views_month').text
    except:
        views = ''
    return views