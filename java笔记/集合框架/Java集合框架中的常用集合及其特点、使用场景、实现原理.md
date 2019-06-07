# java集合框架中的常用集合及其特点、使用场景、实现原理 

Java提供的众多集合类由两大接口衍生而来：Collection接口和Map接口

## Collection接口

Collection接口定义了一个包含一批对象的集合。接口的主要方法包括：

- size() - 集合内的对象数量
- add(E)/addAll(Collection) - 向集合内添加单个/批量对象
- remove(Object)/removeAll(Collection) - 从集合内删除单个/批量对象
- contains(Object)/containsAll(Collection) - 判断集合中是否存在某个/某些对象
- toArray() - 返回包含集合内所有对象的数组

等

## Map接口

Map接口在Collection的基础上，为其中的每个对象指定了一个key，并使用Entry保存每个key-value对，以实现通过key快速定位到对象(value)。Map接口的主要方法包括：

- size() - 集合内的对象数量
- put(K,V)/putAll(Map) - 向Map内添加单个/批量对象
- get(K) - 返回Key对应的对象
- remove(K) - 删除Key对应的对象
- keySet() - 返回包含Map中所有key的Set
- values() - 返回包含Map中所有value的Collection
- entrySet() - 返回包含Map中所有key-value对的EntrySet
- containsKey(K)/containsValue(V) - 判断Map中是否存在指定key/value
  等

在了解了Collection和Map两大接口之后，我们再来看一下这两个接口衍生出来的常用集合类：

## List类集合

![img](http://img.blog.csdn.net/20170519222134334)

List接口继承自Collection，用于定义以列表形式存储的集合，List接口为集合中的每个对象分配了一个索引(index)，标记该对象在List中的位置，并可以通过index定位到指定位置的对象。

List在Collection基础上增加的主要方法包括：

- get(int) - 返回指定index位置上的对象
- add(E)/add(int, E) - 在List末尾/指定index位置上插入一个对象
- set(int, E) - 替换置于List指定index位置上的对象
- indexOf(Object) - 返回指定对象在List中的index位置
- subList(int,int) - 返回指定起始index到终止index的子List对象

等

**List接口的常用实现类：**

## ArrayList

ArrayList基于数组来实现集合的功能，其内部维护了一个可变长的对象数组，集合内所有对象存储于这个数组中，并实现该数组长度的动态伸缩

ArrayList使用数组拷贝来实现指定位置的插入和删除：

插入：

![img](http://img.blog.csdn.net/20170519222940194)

删除：

![img](http://img.blog.csdn.net/20170519223509384)

## LinkedList

LinkedList基于链表来实现集合的功能，其实现了静态类Node，集合中的每个对象都由一个Node保存，每个Node都拥有到自己的前一个和后一个Node的引用

LinkedList追加元素的过程示例：

![img](http://img.blog.csdn.net/20170519224130481)

## ArrayList vs LinkedList

ArrayList的随机访问更高，基于数组实现的ArrayList可直接定位到目标对象，而LinkedList需要从头Node或尾Node开始向后/向前遍历若干次才能定位到目标对象
LinkedList在头/尾节点执行插入/删除操作的效率比ArrayList要高
由于ArrayList每次扩容的容量是当前的1.5倍，所以LinkedList所占的内存空间要更小一些
二者的遍历效率接近，但需要注意，遍历LinkedList时应用iterator方式，不要用get(int)方式，否则效率会很低

## Vector

Vector和ArrayList很像，都是基于数组实现的集合，它和ArrayList的主要区别在于

- Vector是线程安全的，而ArrayList不是
- 由于Vector中的方法基本都是synchronized的，其性能低于ArrayList
- Vector可以定义数组长度扩容的因子，ArrayList不能

## CopyOnWriteArrayList

- 与 Vector一样，CopyOnWriteArrayList也可以认为是ArrayList的线程安全版，不同之处在于 CopyOnWriteArrayList在写操作时会先复制出一个副本，在新副本上执行写操作，然后再修改引用。这种机制让 CopyOnWriteArrayList可以对读操作不加锁，这就使CopyOnWriteArrayList的读效率远高于Vector。 CopyOnWriteArrayList的理念比较类似读写分离，适合读多写少的多线程场景。但要注意，CopyOnWriteArrayList只能保证数据的最终一致性，并不能保证数据的实时一致性，如果一个写操作正在进行中且并未完成，此时的读操作无法保证能读到这个写操作的结果。
- - 二者均是线程安全的、基于数组实现的List
  - Vector是【绝对】线程安全的，CopyOnWriteArrayList只能保证读线程会读到【已完成】的写结果，但无法像Vector一样实现读操作的【等待写操作完成后再读最新值】的能力
  - CopyOnWriteArrayList读性能远高于Vector，并发线程越多优势越明显
  - CopyOnWriteArrayList占用更多的内存空间

# Map类集合 

Map将key和value封装至一个叫做Entry的对象中，Map中存储的元素实际是Entry。只有在keySet()和values()方法被调用时，Map才会将keySet和values对象实例化。

每一个Map根据其自身特点，都有不同的Entry实现，以对应Map的内部类形式出现。

前文已经对Map接口的基本特点进行过描述，我们直接来看一下Map接口的常用实现

## HashMap

HashMap将Entry对象存储在一个数组中，并通过哈希表来实现对Entry的快速访问：

![img](http://img.blog.csdn.net/20170519231809958)

由每个Entry中的key的哈希值决定该Entry在数组中的位置。以这种特性能够实现通过key快速查找到Entry，从而获得该key对应的value。在不发生哈希冲突的前提下，查找的时间复杂度是O(1)。

如果两个不同的key计算出的index是一样的，就会发生两个不同的key都对应到数组中同一个位置的情况，也就是所谓的哈希冲突。HashMap处理哈 希冲突的方法是拉链法，也就是说数组中每个位置保存的实际是一个Entry链表，链表中每个Entry都拥有指向链表中后一个Entry的引用。在发生哈希冲突时，将冲突的Entry追加至链表的头部。当HashMap在寻址时发现某个key对应的数组index上有多个Entry，便会遍历该位置上的 Entry链表，直到找到目标的Entry。

![img](http://img.blog.csdn.net/20170519231953039)

HashMap的Entry类：

```
static class Entry<K,V> implements Map.Entry<K,V> {
        final K key;
        V value;
        Entry<K,V> next;
        int hash;
}

```

HashMap由于其快速寻址的特点，可以说是最经常被使用的Map实现类

## Hashtable

Hashtable 可以说是HashMap的前身（Hashtable自JDK1.0就存在，而HashMap乃至整个Map接口都是JDK1.2引入的新特性），其实现思 路与HashMap几乎完全一样，都是通过数组存储Entry，以key的哈希值计算Entry在数组中的index，用拉链法解决哈希冲突。二者最大的不同在于，Hashtable是线程安全的，其提供的方法几乎都是同步的。

## ConcurrentHashMap

ConcurrentHashMap是HashMap的线程安全版（自JDK1.5引入），提供比Hashtable更高效的并发性能。

![img](https://shirukai.gitee.io/images/wKioL1kcD8mSvKdzAACD-dQPJ_8591.png)

Hashtable 在进行读写操作时会锁住整个Entry数组，这就导致数据越多性能越差。而ConcurrentHashMap使用分离锁的思路解决并发性能，其将 Entry数组拆分至16个Segment中，以哈希算法决定Entry应该存储在哪个Segment。这样就可以实现在写操作时只对一个Segment 加锁，大幅提升了并发写的性能。

在进行读操作时，ConcurrentHashMap在绝大部分情况下都不需要加锁，其Entry中的value是volatile的，这保证了value被修改时的线程可见性，无需加锁便能实现线程安全的读操作。

ConcurrentHashMap的HashEntry类：

```
static final class HashEntry<K,V> {
        final int hash;
        final K key;
        volatile V value;
        volatile HashEntry<K,V> next;
}

```

但是鱼与熊掌不可兼得，ConcurrentHashMap的高性能是有代价的（否则Hashtable就没有存在价值了），那就是它不能保证读操作的绝对 一致性。ConcurrentHashMap保证读操作能获取到已存在Entry的value的最新值，同时也能保证读操作可获取到已完成的写操作的内容，但如果写操作是在创建一个新的Entry，那么在写操作没有完成时，读操作是有可能获取不到这个Entry的。

## HashMap vs Hashtable vs ConcurrentHashMap

> 三者在数据存储层面的机制原理基本一致
> HashMap不是线程安全的，多线程环境下除了不能保证数据一致性之外，还有可能在rehash阶段引发Entry链表成环，导致死循环
> Hashtable是线程安全的，能保证绝对的数据一致性，但性能是问题，并发线程越多，性能越差
> ConcurrentHashMap 也是线程安全的，使用分离锁和volatile等方法极大地提升了读写性能，同时也能保证在绝大部分情况下的数据一致性。但其不能保证绝对的数据一致性， 在一个线程向Map中加入Entry的操作没有完全完成之前，其他线程有可能读不到新加入的Entry

## LinkedHashMap

LinkedHashMap与HashMap非常类似，唯一的不同在于前者的Entry在HashMap.Entry的基础上增加了到前一个插入和后一个插入的Entry的引用，以实现能够按Entry的插入顺序进行遍历。

![img](https://shirukai.gitee.io/images/wKiom1kcEA2yXgx7AAAbvM2NW0k811.png)

图片.png

## TreeMap

TreeMap是基于红黑树实现的Map结构，其Entry类拥有到左/右叶子节点和父节点的引用，同时还记录了自己的颜色：

```
static final class Entry<K,V> implements Map.Entry<K,V> {
        K key;
        V value;
        Entry<K,V> left = null;
        Entry<K,V> right = null;
        Entry<K,V> parent;
        boolean color = BLACK;

}

```

红黑树实际是一种算法复杂但高效的平衡二叉树，具备二叉树的基本性质，即任何节点的值大于其左叶子节点，小于其右叶子节点，利用这种特性，TreeMap能够实现Entry的排序和快速查找。

关于红黑树的具体介绍，可以参考这篇文章，非常详细：<http://blog.csdn.net/chenssy/article/details/26668941>

TreeMap的Entry是有序的，所以提供了一系列方便的功能，比如获取以升序或降序排列的KeySet(EntrySet)、获取在指定key(Entry)之前/之后的key(Entry)等等。适合需要对key进行有序操作的场景。

## ConcurrentSkipListMap

ConcurrentSkipListMap同样能够提供有序的Entry排列，但其实现原理与TreeMap不同，是基于跳表(SkipList)的：

![img](https://shirukai.gitee.io/images/wKiom1kcEEzR4gVTAAEH57HmPIo744.png)

如上图所示，ConcurrentSkipListMap由一个多级链表实现，底层链上拥有所有元素，逐级上升的过程中每个链的元素数递减。在查找时从顶层链出发，按先右后下的优先级进行查找，从而实现快速寻址。

```
static class Index<K,V> {
        final Node<K,V> node;
        final Index<K,V> down;//下引用
        volatile Index<K,V> right;//右引用
}

```

与TreeMap不同，ConcurrentSkipListMap在进行插入、删除等操作时，只需要修改影响到的节点的右引用，而右引用又是volatile的，所以ConcurrentSkipListMap是线程安全的。但ConcurrentSkipListMap与ConcurrentHashMap一样，不能保证数据的绝对一致性，在某些情况下有可能无法读到正在被插入的数据。

## TreeMap vs ConcurrentSkipListMap

二者都能够提供有序的Entry集合
二者的性能相近，查找时间复杂度都是O(logN)
ConcurrentSkipListMap会占用更多的内存空间
ConcurrentSkipListMap是线程安全的，TreeMap不是

## Set类集合

Set 接口继承Collection，用于存储不含重复元素的集合。几乎所有的Set实现都是基于同类型Map的，简单地说，Set是阉割版的Map。每一个Set内都有一个同类型的Map实例（CopyOnWriteArraySet除外，它内置的是CopyOnWriteArrayList实例），Set把元素作为key存储在自己的Map实例中，value则是一个空的Object。Set的常用实现也包括 HashSet、TreeSet、ConcurrentSkipListSet等，原理和对应的Map实现完全一致，此处不再赘述。

![img](https://shirukai.gitee.io/images/wKioL1kcEInwh_vIAAGRszBvREo466.png)

图片.png

## Queue/Deque类集合

![img](https://shirukai.gitee.io/images/wKioL1kcEKiDPKU7AAJY5VAswno664.png)

Queue和Deque接口继承Collection接口，实现FIFO（先进先出）的集合。二者的区别在于，Queue只能在队尾入队，队头出队，而Deque接口则在队头和队尾都可以执行出/入队操作

Queue接口常用方法：

- add(E)/offer(E)：入队，即向队尾追加元素，二者的区别在于如果队列是有界的，add方法在队列已满的情况下会抛出IllegalStateException，而offer方法只会返回false
- remove()/poll()：出队，即从队头移除1个元素，二者的区别在于如果队列是空的，remove方法会抛出NoSuchElementException，而poll只会返回null
- element()/peek()：查看队头元素，二者的区别在于如果队列是空的，element方法会抛出NoSuchElementException，而peek只会返回null

Deque接口常用方法：

- addFirst(E) / addLast(E) / offerFirst(E) / offerLast(E)
- removeFirst() / removeLast() / pollFirst() / pollLast()
- getFirst() / getLast() / peekFirst() / peekLast()
- removeFirstOccurrence(Object) / removeLastOccurrence(Object)

Queue接口的常用实现类：

## ConcurrentLinkedQueue

ConcurrentLinkedQueue是基于链表实现的队列，队列中每个Node拥有到下一个Node的引用：

```
private static class Node<E> {
        volatile E item;
        volatile Node<E> next;
}

```

由于Node类的成员都是volatile的，所以ConcurrentLinkedQueue自然是线程安全的。能够保证入队和出队操作的原子性和一致性，但在遍历和size()操作时只能保证数据的弱一致性。

## LinkedBlockingQueue

与ConcurrentLinkedQueue不同，LinkedBlocklingQueue是一种无界的阻塞队列。所谓阻塞队列，就是在入队时如果队列已满，线程会被阻塞，直到队列有空间供入队再返回；同时在出队时，如果队列已空，线程也会被阻塞，直到队列中有元素供出队时再返回。LinkedBlocklingQueue同样基于链表实现，其出队和入队操作都会使用ReentrantLock进行加锁。所以本身是线程安全的，但同样的，只能保证入队和出队操作的原子性和一致性，在遍历时只能保证数据的弱一致性。

## ArrayBlockingQueue

ArrayBlockingQueue是一种有界的阻塞队列，基于数组实现。其同步阻塞机制的实现与LinkedBlocklingQueue基本一致，区别仅在于前者的生产和消费使用同一个锁，后者的生产和消费使用分离的两个锁。

ConcurrentLinkedQueue vsLinkedBlocklingQueue vs ArrayBlockingQueue

ConcurrentLinkedQueue是非阻塞队列，其他两者为阻塞队列
三者都是线程安全的
LinkedBlocklingQueue是无界的，适合实现不限长度的队列， ArrayBlockingQueue适合实现定长的队列

## SynchronousQueue

SynchronousQueue算是JDK实现的队列中比较奇葩的一个，它不能保存任何元素，size永远是0，peek()永远返回null。向其中插入元素的线程会阻塞，直到有另一个线程将这个元素取走，反之从其中取元素的线程也会阻塞，直到有另一个线程插入元素。

这种实现机制非常适合传递性的场景。也就是说如果生产者线程需要及时确认到自己生产的任务已经被消费者线程取走后才能执行后续逻辑的场景下，适合使用SynchronousQueue。

## PriorityQueue & PriorityBlockingQueue

这两种Queue并不是FIFO队列，而是根据元素的优先级进行排序，保证最小的元素最先出队，也可以在构造队列时传入Comparator实例，这样PriorityQueue就会按照Comparator实例的要求对元素进行排序。

PriorityQueue是非阻塞队列，也不是线程安全的，PriorityBlockingQueue是阻塞队列，同时也是线程安全的。

Deque 的实现类包括LinkedList（前文已描述过）、ConcurrentLinkedDeque、LinkedBlockingDeque，其实现机制与前文所述的ConcurrentLinkedQueue和LinkedBlockingQueue非常类似，此处不再赘述

最后，对本文中描述的常用集合实现类做一个简单总结：

![img](https://shirukai.gitee.io/images/wKiom1kcESOicSLfAAIVQl371Y0815.png)