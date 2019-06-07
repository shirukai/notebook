# jpa利用pageable分页排序 

```
@RequestMapping(value = "/testPageable", method = RequestMethod.GET)
public Page<User> testPageable(
        @RequestParam("page") Integer page,
        @RequestParam("size") Integer size,
        @RequestParam("sortType") String sortType,
        @RequestParam("sortableFields") String sortableFields
) {
    //判断排序类型及排序字段
    Sort sort = "ASC".equals(sortType) ? new Sort(Sort.Direction.ASC, sortableFields) : new Sort(Sort.Direction.DESC, sortableFields);
    //获取pageable
    Pageable pageable = new PageRequest(page-1,size,sort);
    return userRepository.findAll(pageable);

}
```

参考博客：http://blog.csdn.net/u011848397/article/details/52151673